import pytest
from faker import Faker
from client_ui_components import QueryHandler  # Replace with actual module name
import random
import json
@pytest.fixture
def query_handler():
    return QueryHandler(
        update_ui_callback=(mock_callback),  # Replace with your UI callback function
        h2_path="../../../Client/Cache/h2-1.4.200.jar",
        lexer_parser_path = "../../../Client/LexerParser/main"
    )

def test_create_100_people(query_handler):
    query_handler.populate_graph(100)

    # Assert that the count of people is 100
    # Replace with actual method to retrieve results from your query handler
    count_result = query_handler.get_last_query_result()
    response = json.loads(count_result)
    assert 100 in response[0]['Values']

    # Extract the count result
    # Replace with actual method to retrieve results from your query handler
    return query_handler.get_last_query_result()



def mock_callback(num, response, tags):
    pass
