from authentication.user import User
from database.db import Database
import bcrypt

# This class manages the operators's login procedure
class Login():

    def __init__(self):
        # Authorization database contains the operators table
        self.db = Database()

    def validate_user(self, username, password):
        # Find operator by credentials
        cur = self.db.query("""
                            SELECT Password, IS_admin, Action_permissions, Table_permissions FROM operators 
                            WHERE Username = %s""",
                            [username])

        # Fetch one row with pertinent information
        r = cur.fetchone()

        # If the operator was not found, he/she must have provided incorrect credentials
        if not r:
            return {"status": "failed", "details": "Username/password incorrect"}

        # Get the password hash from database
        db_hash = r[0].encode()

        # Check that the hash and the given password match
        if bcrypt.checkpw(password.encode(), db_hash):
            # Return the success code along with the populated User object            
            return {"status": "success", "user": User(username, r[1], r[2], r[3])}

        return {"status": "failed", "details": "Username/password incorrect"}
