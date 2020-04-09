import MySQLdb
from server.server_config import ServerConfig

class Database:

    def __init__(self, key):
        self.key = key

    def connect(self):
        conn = MySQLdb.connect(host=ServerConfig().get_config()[self.key]['host'],
                                port=ServerConfig().get_config()[self.key]['port'],
                                user=ServerConfig().get_config()[self.key]['username'],
                                passwd=ServerConfig().get_config()[self.key]['password'],
                                db=ServerConfig().get_config()[self.key]['db'])

        conn.autocommit(True)
        return conn

    def query(self, sql, args=None):
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(sql,args)

            conn.close()
            return cursor

    def query_many(self, sql, args=None):
            conn = self.connect()
            cursor = conn.cursor()
            cursor.executemany(sql,args)
            
            conn.close()
            return cursor
