from authentication.user import User
from database.db import Database

class Login():

    def __init__(self):
        self.db = Database('auth_db')

    def validate_user(self, username, password):
        cur = self.db.query("""
                            SELECT IS_admin, Action_permissions, Table_permissions FROM operators WHERE
                            Username = %s AND Password = %s;""",
                            [username, password])

        r = cur.fetchone()

        if not r:
            return {"status": "failed", "details": "Username/password incorrect"}

        print(r[0])                    
        return {"status": "success", "user": User(username, r[0], r[1], r[2])}
        
