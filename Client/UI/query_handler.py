import subprocess
import http
import requests
import json
from h2_cache import H2Cache

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
            # check if query is cached and return if so
            self.is_write = self.is_write_query(query)
            if (cached_query := self.cache.execute_query(query, self.is_write)):
                result = cached_query
                tag = "success"
            # else execute query on neo4j database and return result
            else:
                try:
                    response = self.send_neo4j_query("{0}".format(query))
                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        # Parse the response content as needed
                        result = response.text
                        tag = "success"
                        self.cache.cache_result(query=query, result=result)

                    else:
                        result = f"HTTP Error {response.status_code}: {response.text}"
                        tag = "error"

                except Exception as e:
                    result = (f"An error occurred: {str(e)}")
                    tag = "error"

        self.ui_callback("0.0", f"{result}\n", tags=[tag])

    def send_neo4j_query(self, neo4j_query):
            # create a dictionary with the neo4j query as the payload
            payload = {"query": neo4j_query, "isWrite": self.is_write}
            json_data = json.dumps(payload)

            # send an HTTP POST request to the specified URL
            response = requests.post("http://localhost:8080/query", data=json_data)
            return response

    def is_write_query(self, query):
        write_keywords = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE", "DETACH DELETE", "CALL"]
        for keyword in write_keywords:
            if keyword in query.upper():
                return True
        return False


