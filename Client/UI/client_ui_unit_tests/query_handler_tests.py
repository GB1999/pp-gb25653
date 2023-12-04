import pytest
from unittest.mock import Mock, patch
import subprocess
import requests
from client_ui_components import QueryHandler

@pytest.fixture
def query_handler():
    update_ui_callback = Mock()
    h2_path = "../../Cache/h2-1.4.200.jar"
    lexer_parser_path = "../../LexerParser/main"
    return QueryHandler(update_ui_callback, h2_path, lexer_parser_path)

def test_parser_failure(query_handler):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stderr="Parser Error")
        query_handler.submit_query('CATCH (:Person {name: "Alice", age: 25})')
        query_handler.ui_callback.assert_called_with("0.0", "Parser Error\n", tags=["error"])

def test_cached_query(query_handler):
    query = 'create (:Person {name: "Alice", age: 25});'
    cached_result = "Cached Result"
    with patch.object(query_handler.cache, 'execute_query', return_value=cached_result):
        query_handler.submit_query(query)
        # check ui_callback invocation has "cached" tag
        query_handler.ui_callback.assert_called_with("0.0", f"{cached_result}\n", tags=["success", "cached"])


def test_neo4j_query_success(query_handler):
    query = 'MATCH (p:Person {name: "John"}) RETURN p'
    response_text = "Response Text"
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock(status_code=200, text=response_text)
        query_handler.submit_query(query)
        query_handler.ui_callback.assert_called_with("0.0", f"{response_text}\n", tags=["success"])

# test to ensure that cache is cleared when writing
def test_write_query_cache_clearing(query_handler):
    write_query = "CREATE (n:Person {name: 'Alice'})"
    with patch('requests.post') as mock_post, \
        patch.object(query_handler.cache, 'clear_cache') as mock_clear_cache:
        mock_post.return_value = Mock(status_code=200, text="Write Success")
        query_handler.submit_query(write_query)
        mock_clear_cache.assert_called_once()

# check to test whether is_write can distinguish between read and write cypher queries
@pytest.mark.parametrize("query,expected", [
    ("CREATE (n:Person {name: 'Alice'})", True),
    ("MATCH (n) RETURN n", False),
])

def test_is_write_query(query_handler, query, expected):
    assert query_handler.is_write_query(query) == expected


