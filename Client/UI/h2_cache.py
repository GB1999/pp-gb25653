import sqlite3
import hashlib
import jaydebeapi

class H2Cache:
    def __init__(self, h2_jar_file):
        self.h2_conn = jaydebeapi.connect('org.h2.Driver', 'jdbc:h2:~/test', ['sa', ''], h2_jar_file)
        self.create_cache_table()

    def create_cache_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS query_cache (
            query VARCHAR(1024),
            result VARCHAR(65535)
        );
        """
        cursor = self.h2_conn.cursor()
        cursor.execute(create_table_sql)
        cursor.close()

    def close_connections(self):
        self.h2_conn.close()

    def cache_result(self, query, result):
        cursor = self.h2_conn.cursor()
        cursor.execute("INSERT INTO query_cache (query, result) VALUES (?, ?)", (query, str(result)))
        cursor.close()

    def get_cached_result(self, query):
        cursor = self.h2_conn.cursor()
        cursor.execute("SELECT result FROM query_cache WHERE query = ?", (query,))
        result = cursor.fetchone()
        print(result)
        cursor.close()
        return eval(result[0]) if result else None

    def clear_cache(self):
        cursor = self.h2_conn.cursor()
        cursor.execute("DELETE FROM query_cache")
        cursor.close()

    def execute_query(self, query, is_write):
        if is_write:
            return None

        cached_result = self.get_cached_result(query)
        return cached_result


