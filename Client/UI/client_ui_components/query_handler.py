import subprocess
import http
import requests
import json
from .h2_cache import H2Cache
import random
from faker import Faker
class QueryHandler():
    def __init__(self, update_ui_callback, h2_path, lexer_parser_path):
        self.cache = H2Cache(h2_path)
        self.ui_callback = update_ui_callback
        self.parser_path = lexer_parser_path
        self.is_write: bool
        self.tags: [str]
    def submit_query(self, query):
        self.tags = []
        #check for invalid query using go lexer/parser
        output = subprocess.run([self.parser_path, query], capture_output=True, text=True)
        if (output.stderr):
            result = output.stderr
            self.tags = ["error"]

        else:
            # check if query is cached and return if so. write queries will return None
            is_write = self.is_write_query(query)
            if (cached_query := self.cache.execute_query(query, is_write)):
                result = cached_query
                self.tags = ["success", "cached"]
            # else execute query on neo4j database and return result
            else:
                try:
                    response = self.send_neo4j_query("{0}".format(query), is_write)
                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        result = response.text
                        self.tags = ["success"]

                        # delete current cache if write is successful
                        if is_write:
                            self.cache.clear_cache()
                            self.restructure_response(result)
                        # update cache if read is successful
                        else:
                            self.cache.cache_result(query=query, result=result)

                    else:
                        result = f"HTTP Error {response.status_code}: {response.text}"
                        self.tags = ["error"]

                except Exception as e:
                    result = (f"An error occurred: {str(e)}")
                    tag = "error"

        self.result = result
        self.ui_callback("0.0", f"{result}\n", tags=self.tags)

    def send_neo4j_query(self, neo4j_query, is_write_query):
            # create a dictionary with the neo4j query as the payload
            payload = {"query": neo4j_query, "isWrite": is_write_query}
            json_data = json.dumps(payload)

            # send an HTTP POST request to the specified URL
            response = requests.post("http://localhost:8080/query", data=json_data)
            return response

    def clear_neo4j_graph(self):
        self.submit_query('MATCH (n) DETACH DELETE n')

    def populate_graph(self, n):
        fake = Faker()

        # clear the existing data
        self.clear_neo4j_graph()
        people = []

        # generate and submit queries for n random people using Faker
        for i in range(n):
            name = fake.name()
            age = fake.random_int(min=18, max=100)
            person_id = f"Person_{fake.uuid4()}"  # Unique identifier for each person
            people.append({'name': name, 'id': person_id})
            create_query = f'CREATE (:Person {{name: "{name}", age: {age}}});'
            self.write_query_to_file(create_query)
            self.submit_query(create_query)

        # assign friendships
        for person in people:
            number_of_friends = random.randint(1, 5)  # Each person will have 1 to 5 friends
            friends = random.sample([p for p in people if p != person], number_of_friends)

            for friend in friends:
                create_friendship_query = 'MATCH (a:Person {{name: "{0}"}}), (b:Person {{name: "{1}"}}) CREATE (a)-[:Friend]->(b);'.format(
                    person['name'], friend['name'])
                self.submit_query(create_friendship_query)

        # perform a read query to count the number of people
        count_people_query = 'MATCH (p:Person) RETURN count(p) as total;'
        self.submit_query(count_people_query)

    def get_last_query_result(self):
        return self.result

    # check query for write keywords
    def is_write_query(self, query):
        write_keywords = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE", "DETACH DELETE", "CALL"]
        for keyword in write_keywords:
            if keyword in query.upper():
                return True
        return False
    # "prettify" response for easier parsing in visualizer(s)
    def restructure_response(self, response):
        if response == "null" or response is None:
            return
        # parse neo4j response to json object
        graph = json.loads(response)
        # remove null values
        graph = self.clean_nones(graph)

        nodes = {}
        edges = {}
        adjacency = {}

        # Process the Neo4j graph data
        for entry in graph:
            for value in entry["Values"]:
                if "Labels" in value and "Person" in value["Labels"]:
                    # Add node
                    node_id = value["Id"]
                    nodes[node_id] = {"name": value["Props"]["name"], "age": value["Props"]["age"]}

                elif "Type" in value and "Friend" in value["Type"]:
                    # Add edge
                    edge_id = value["Id"]
                    from_id = value["StartId"]
                    to_id = value["EndId"]
                    edges[edge_id] = {"from": str(from_id), "to": str(to_id), "type": "Friend"}
                    # Update adjacency list
                    #adjacency[from_id].append(to_id)

        # construct the final graph structure in the desired format
        adjacency_list_graph = {
            "Graph": {
                "adjacency": adjacency,
                "nodes": nodes,
                "edges": edges
            }
        }

        # convert the graph to a JSON string
        json_graph = json.dumps(adjacency_list_graph, indent=3)
        # write the JSON string to a file
        with open("../../Visualizer/graph.json", 'w') as file:
            file.write(json_graph)
            file.close()

    # recursively remove all None values from dictionaries and lists
    # returns the result as a new dictionary or list.
    def clean_nones(self, value):
        # check if value is list and remove all null values
        if isinstance(value, list):
            return [self.clean_nones(x) for x in value if x is not None]
        # else recursively call clean_nones on each value in the map
        elif isinstance(value, dict):
            return {
                key: self.clean_nones(val)
                for key, val in value.items()
                if val is not None
            }
        # base case
        else:
            return value

    def write_query_to_file(self, query, file_path='generated_queries.txt'):
        with open(file_path, 'a') as file:
            file.write(query + '\n')