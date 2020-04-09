from authentication.user import User
from fastapi import HTTPException

class Permissions:

    def validate_action(self, user, action, table=None):
        if user.is_admin:
            return

        if action != 'all' and action not in user.action_permissions:
            raise HTTPException(status_code=403, detail="Action forbidden")

        if table and table not in user.table_permissions or table == 'operators':
            raise HTTPException(status_code=403, detail="Access to table forbidden")
