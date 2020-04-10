import MySQLdb
from server.server_config import ServerConfig

# This class is used to connect to a MySQL database and query it
class Database:

    def __init__(self, key):
        # The key refers to a key in the server config YAML file
        # under which the database host, port, username, password,
        # and database name will be given.
        self.key = key

    # Connect to the database and return the connector object
    def connect(self):
        # Connect to db given credentials in the config file
        conn = MySQLdb.connect(host=ServerConfig().get_config()[self.key]['host'],
                                port=ServerConfig().get_config()[self.key]['port'],
                                user=ServerConfig().get_config()[self.key]['username'],
                                passwd=ServerConfig().get_config()[self.key]['password'],
                                db=ServerConfig().get_config()[self.key]['db'])

        # Changes made during code execution will automatically commit to the server
        conn.autocommit(True)
        return conn

    # Execute with one set of parameters being passed into the SQL statement
    def query(self, sql, args=None):
            # Open and close the connection per call in case server settings in the
            # config file changed
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(sql,args)

            conn.close()
            return cursor

    # Iterates through a sequence of parameters and passes each to the execute
    def query_many(self, sql, args=None):
            conn = self.connect()
            cursor = conn.cursor()
            cursor.executemany(sql,args)
            
            conn.close()
            return cursor
