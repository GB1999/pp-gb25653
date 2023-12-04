import pytest
from unittest.mock import Mock, patch, MagicMock
from client_ui_components import H2Cache  # Replace 'your_module' with the actual name of the module where H2Cache is defined

class TestH2Cache:

    @pytest.fixture
    def mock_db_connection(self):
        with patch('jaydebeapi.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_conn
            yield mock_conn, mock_cursor

    def test_init(self, mock_db_connection):
        mock_conn, mock_cursor = mock_db_connection
        h2_jar_file = '../../Client/Cache/h2-1.4.200.jar'
        cache = H2Cache(h2_jar_file)
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        assert cache.h2_conn is mock_conn

    def test_create_cache_table(self, mock_db_connection):
        mock_conn, mock_cursor = mock_db_connection
        cache = H2Cache('../../Client/Cache/h2-1.4.200.jar')
        cache.create_cache_table()
        mock_cursor.execute.assert_called()
        assert 'CREATE TABLE IF NOT EXISTS query_cache' in mock_cursor.execute.call_args[0][0]

    def test_close_connections(self, mock_db_connection):
        mock_conn, _ = mock_db_connection
        cache = H2Cache('../../Cache/h2-1.4.200.jar')
        cache.close_connections()
        mock_conn.close.assert_called_once()

    def test_cache_result(self, mock_db_connection):
        mock_conn, mock_cursor = mock_db_connection
        cache = H2Cache('../../Client/Cache/h2-1.4.200.jar')
        test_query = 'SELECT * FROM test'
        test_result = 'Test Result'
        cache.cache_result(test_query, test_result)
        mock_cursor.execute.assert_called_with("INSERT INTO query_cache (query, result) VALUES (?, ?)", (test_query, str(test_result)))

    def test_get_cached_result(self, mock_db_connection):
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = ('{"data": "test"}',)
        cache = H2Cache('../../Client/Cache/h2-1.4.200.jar')
        test_query = 'SELECT * FROM test'
        result = cache.get_cached_result(test_query)
        mock_cursor.execute.assert_called_with("SELECT result FROM query_cache WHERE query = ?", (test_query,))
        assert result == {"data": "test"}

    def test_clear_cache(self, mock_db_connection):
        mock_conn, mock_cursor = mock_db_connection
        cache = H2Cache('../../../Client/Cache/h2-1.4.200.jar')
        cache.clear_cache()
        mock_cursor.execute.assert_called_with("DELETE FROM query_cache")

    def test_execute_query_write(self, mock_db_connection):
        cache = H2Cache('../../../Client/Cache/h2-1.4.200.jar')
        write_query = 'INSERT INTO test (data) VALUES ("data")'
        result = cache.execute_query(write_query, is_write=True)
        assert result is None

    def test_execute_query_read(self, mock_db_connection):
        mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchone.return_value = ('{"data": "test"}',)
        cache = H2Cache('../../Client/Cache/h2-1.4.200.jar')
        read_query = 'SELECT * FROM test'
        result = cache.execute_query(read_query, is_write=False)
        assert result == {"data": "test"}
