import MySQLdb
from server.server_config import ServerConfig

# This class is used to connect to a MySQL database and query it
class Database:

    # Connect to the database and return the connector object
    def connect(self):
        # Connect to db given credentials in the config file
        conn = MySQLdb.connect(host=ServerConfig().get_config()['mysql']['host'],
                                port=ServerConfig().get_config()['mysql']['port'],
                                user=ServerConfig().get_config()['mysql']['username'],
                                passwd=ServerConfig().get_config()['mysql']['password'],
                                db=ServerConfig().get_config()['mysql']['db'])

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
