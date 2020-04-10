from authentication.user import User
from database.db import Database

# This class manages the operators's login procedure
class Login():

    def __init__(self):
        # Authorization database contains the operators table
        self.db = Database('auth_db')

    def validate_user(self, username, password):
        # Find operator by credentials
        cur = self.db.query("""
                            SELECT IS_admin, Action_permissions, Table_permissions FROM operators WHERE
                            Username = %s AND Password = %s;""",
                            [username, password])

        # Fetch one row with pertinent information
        r = cur.fetchone()

        # If the operator was not found, he/she must have provided incorrect credentials
        if not r:
            return {"status": "failed", "details": "Username/password incorrect"}

        # Return the success code along with the populated User object            
        return {"status": "success", "user": User(username, r[0], r[1], r[2])}
        
