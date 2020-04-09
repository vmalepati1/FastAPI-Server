from authentication.user import User
from fastapi import HTTPException

class Permissions:

    def validate_action(self, user, action, table=None):
        if table == 'operators':
            raise HTTPException(status_code=403, detail="Access to table forbidden")
        
        if user.is_admin:
            return

        if user.action_permissions != 'all' and action not in user.action_permissions:
            raise HTTPException(status_code=403, detail="Action forbidden")

        if table and table not in user.table_permissions:
            raise HTTPException(status_code=403, detail="Table does not exist or access to table forbidden")
