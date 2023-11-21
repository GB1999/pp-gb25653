import subprocess
import http
import requests
import json
from .h2_cache import H2Cache

class QueryHandler():
    def __init__(self, update_ui_callback, h2_path, lexer_parser_path):
        self.cache = H2Cache(h2_path)
        self.ui_callback = update_ui_callback
        self.parser_path = lexer_parser_path
        self.is_write: bool
    def submit_query(self, query):
        #check for invalid query using go lexer/parser
        output = subprocess.run([self.parser_path, query], capture_output=True, text=True)
        if (output.stderr):
            result = output.stderr
            tag = "error"

        else:
            # check if query is cached and return if so. write queries will return None
            is_write = self.is_write_query(query)
            if (cached_query := self.cache.execute_query(query, is_write)):
                result = cached_query
                tag = "success"
            # else execute query on neo4j database and return result
            else:
                try:
                    response = self.send_neo4j_query("{0}".format(query), is_write)
                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        result = response.text
                        tag = "success"

                        # delete current cache if write is successful
                        if is_write:
                            self.cache.clear_cache()
                            self.restructure_response(result)
                        # update cache if read is successful
                        else:
                            self.cache.cache_result(query=query, result=result)

                    else:
                        result = f"HTTP Error {response.status_code}: {response.text}"
                        tag = "error"

                except Exception as e:
                    result = (f"An error occurred: {str(e)}")
                    tag = "error"

        self.ui_callback("0.0", f"{result}\n", tags=[tag])

    def send_neo4j_query(self, neo4j_query, is_write_query):
            # create a dictionary with the neo4j query as the payload
            payload = {"query": neo4j_query, "isWrite": is_write_query}
            json_data = json.dumps(payload)

            # send an HTTP POST request to the specified URL
            response = requests.post("http://localhost:8080/query", data=json_data)
            return response

    def clear_neo4j_graph(self):
        self.submit_query('MATCH (n) DETACH DELETE n')

    def is_write_query(self, query):
        write_keywords = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE", "DETACH DELETE", "CALL"]
        for keyword in write_keywords:
            if keyword in query.upper():
                return True
        return False

    def restructure_response(self, response):

        if response == "null" or response is None:
            return

        print("//////NEO4J REPONSE//////")
        print(response)

        graph = json.loads(response)
        graph = self.clean_nones(graph)

        nodes = {}
        edges = {}
        adjacency = {}

        # Process the Neo4j graph data
        for entry in graph:
            print(entry)
            for value in entry["Values"]:
                if "Labels" in value and "Person" in value["Labels"]:
                    # Add node
                    node_id = value["Id"]
                    nodes[node_id] = {"name": value["Props"]["name"], "age": value["Props"]["age"]}
                    #adjacency[node_id] = []

                elif "Type" in value and "Friend" in value["Type"]:
                    # Add edge
                    edge_id = value["Id"]
                    from_id = value["StartId"]
                    to_id = value["EndId"]
                    edges[edge_id] = {"from": str(from_id), "to": str(to_id), "type": "Friend"}
                    # Update adjacency list
                    #adjacency[from_id].append(to_id)

        # Construct the final graph structure in the desired format
        adjacency_list_graph = {
            "Graph": {
                "adjacency": adjacency,
                "nodes": nodes,
                "edges": edges
            }
        }

        # Convert the graph to a JSON string
        json_graph = json.dumps(adjacency_list_graph, indent=3)
        # Write the JSON string to a file
        with open("../../Visualizer/graph.json", 'w') as file:
            file.write(json_graph)
            file.close()

    def clean_nones(self, value):
        """
        Recursively remove all None values from dictionaries and lists, and returns
        the result as a new dictionary or list.
        """
        if isinstance(value, list):
            return [self.clean_nones(x) for x in value if x is not None]
        elif isinstance(value, dict):
            return {
                key: self.clean_nones(val)
                for key, val in value.items()
                if val is not None
            }
        else:
            return value