from authentication.user import User
from fastapi import HTTPException

# This class performs checks related to operator permissions
class Permissions:

    # Validate an action the operator is taking and raise an exception if it is forbidden
    def validate_action(self, user, action, table=None):
        # No operator may edit the operators table
        if table == 'operators':
            raise HTTPException(status_code=403, detail="Access to table forbidden")

        # Admin bypasses all restrictions
        if user.is_admin:
            return

        # Perform action permission check
        if user.action_permissions != 'all' and action not in user.action_permissions:
            raise HTTPException(status_code=403, detail="Action forbidden")

        # Perform table permission check
        if table and table not in user.table_permissions:
            raise HTTPException(status_code=403, detail="Table does not exist or access to table forbidden")
