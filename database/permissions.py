from authentication.user import User
from fastapi import HTTPException
from database.db import Database

# This class performs checks related to operator permissions
class Permissions:

    def __init__(self):
        # Used to check operator actions
        self.db = Database()

    # Validate an operator's action to view/edit another operator/user
    def validate_operator_access(self, user, other_username):
        if user.IS_admin:
            return

        if user.Username == other_username:
            return

        # Back-reference final users who are related to operator's company
        cur = self.db.query("""SELECT cart.User_ID FROM cart, cart_detail WHERE cart.id = cart_detail.Cart_ID
                                AND cart_detail.Company_ID = %s""",
                            [user.Company_ID])

        # Fetch user ids
        r = cur.fetchall()

        # If no users are related to operator
        if not r:
            raise HTTPException(status_code=403, detail="Cannot access user (no associated final users)")

        usernames = []
        
        for row in r:
            # Convert id to username
            user_id = row[0]
            cur = self.db.query("SELECT Username FROM operators WHERE Operator_ID = %s",
                                [user_id])
            r = cur.fetchone()
            
            # If operator "disappeared"
            if not r:
                raise HTTPException(status_code=500, detail="Cannot find user")

            usernames.append(r[0])

        if not other_username in usernames:
            raise HTTPException(status_code=403, detail="Cannot access user (action forbidden)")
        
    # Validate an action the operator is taking and raise an exception if it is forbidden
    def validate_action(self, user, action, table=None):
        # Admin bypasses all restrictions
        if user.IS_admin:
            return

        # Perform action permission check
        if user.action_permissions and user.action_permissions != 'all' and action not in user.action_permissions:
            raise HTTPException(status_code=403, detail="Action forbidden")

        # Perform table permission check
        if user.table_permissions and table and table not in user.table_permissions:
            raise HTTPException(status_code=403, detail="Table does not exist or access to table forbidden")
