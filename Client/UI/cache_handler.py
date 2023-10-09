
import jaydebeapi
class CacheHandler:
    def connect(self, user, password, jar_dir):
        conn = jaydebeapi.connect("org.h2.Driver", "jdbc:h2:~/test", [user, password],
                                  jar_dir)
        self.curs = conn.cursor()
    def execute(self, command: str):
        self.curs.execute('create table CUSTOMER'
                    '("CUST_ID" INTEGER not null,'
                    ' "NAME" VARCHAR(50) not null,'
                    ' primary key ("CUST_ID"))'
                    )
    def close_cache(self):
        self.curs.close()

    def fetch_all(self):
        self.curs.fetchall()