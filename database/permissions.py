from authentication.user import User
from fastapi import HTTPException
from database.db import Database
from authentication.user import User

# This class performs checks related to operator permissions
class Permissions:

    company_tables = ['category_company_assignment', 'company', 'company_delivery', 'company_timetable', 'cart']

    def __init__(self):
        # Used to check operator actions
        self.db = Database()

    def get_affiliated_final_users(self, company_id):
        # Back-reference final users who are related to operator's company
        try:
            cur = self.db.query("""SELECT cart.User_ID FROM cart WHERE cart.Company_ID = %s""",
                                [company_id])
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
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error: " + str(e))

        return usernames

    # Validate an operator's action to view/edit another operator/user
    def validate_operator_access(self, user, other_username):
        if user.IS_admin:
            return

        if user.Username == other_username:
            return

        if not other_username in self.get_affiliated_final_users(user.Company_ID):
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

    # Restrict reading view based on admin or operator
    def get_restricted_read_query(self, user, what_to_select, which_table, conditions_to_satisfy):
        # Public records bypass all restrictions
        if not user:
            user = User(ia=True)
            
        # Operator can only view his company records
        if not conditions_to_satisfy and not user.IS_admin:
            raise HTTPException(status_code=403, detail="Operator is not allowed to view all records")

        if not conditions_to_satisfy:
            # Admin can view everything
            query = "SELECT {0} FROM {1};".format(what_to_select, which_table)
        else:
            # Default query
            query = "SELECT {0} FROM {1} WHERE {2};".format(what_to_select, which_table, conditions_to_satisfy)

            if not user.IS_admin:
                # Make sure record is affiliated with company id
                if which_table in self.company_tables:
                    query = "SELECT {0} FROM {1} WHERE {2} AND Company_ID = {3};".format(what_to_select, which_table, conditions_to_satisfy, user.Company_ID)

                # Make sure user operator is accessing is affiliated with his company
                if which_table == 'operators':
                    usernames_quotes = ', '.join(["'" + u + "'" for u in self.get_affiliated_final_users(user.Company_ID) if u])
                    query = "SELECT {0} FROM {1} WHERE {2} AND (Company_ID = {3} OR Username IN ({4}));".format(what_to_select, which_table, conditions_to_satisfy,
                                                                                                                user.Company_ID, usernames_quotes)
        return query

    # Validate insert request and ensure operator only adding to his company data
    def validate_insert(self, user, all_columns, columns, values):
        if user.IS_admin:
            return

        if columns:
            if 'Company_ID' in columns:
                cid = values[columns.index('Company_ID')]

                if user.Company_ID != cid:
                    raise HTTPException(status_code=403, detail="Action forbidden")
        else:
            if 'Company_ID' in all_columns:
                cid = values[all_columns.index('Company_ID')]

                if user.Company_ID != cid:
                    raise HTTPException(status_code=403, detail="Action forbidden")
            
    # Validate insert request and ensure operator only editing/deleting his company data
    def validate_edit_delete(self, user, columns, table_name, where_condition):
        if user.IS_admin:
            return

        if not where_condition and not user.IS_admin:
            raise HTTPException(status_code=403, detail="Operator is not allowed to edit all records")

            if table_name == 'operators':
                try:
                    cur = self.db.query("SELECT Username FROM operators WHERE {0};".format(where_condition))

                    # Fetch rows that operator is editing
                    r = cur.fetchall()

                except Exception as e:
                    raise HTTPException(status_code=400, detail="Error: " + str(e))

                usernames = self.get_affiliated_final_users(user.Company_ID)
                        
                for row in r:
                    # Operator not editing himself or editing someone who company is not affiliated with
                    if row[0] != user.Username or row[0] not in usernames:
                        raise HTTPException(status_code=403, detail="Action forbidden")

        if 'Company_ID' in columns:
            try:
                cur = self.db.query("SELECT Company_ID FROM {0} WHERE {1};".format(table_name, where_condition))

                # Fetch rows that operator is editing
                r = cur.fetchall()
            except Exception as e:
                raise HTTPException(status_code=400, detail="Error: " + str(e))
            
            for row in r:
                if row[0] != user.Company_ID:
                    raise HTTPException(status_code=403, detail="Action forbidden")


