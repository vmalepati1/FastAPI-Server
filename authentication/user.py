import jwt
from server.server_config import ServerConfig
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel
import json
from database.db import Database

# This class contains all the necessary information to describe an operator, or user
# The information can be encoded into a JWT token
# The JWT token can also be decoded back to a User object
class User():
    # All fields of operator in database
    operator_fields = ['Operator_ID', 'First_name', 'Last_name', 'Mobile_num',
                       'Mobile_confirmed', 'Email', 'Created_at', 'Modified_at',
                       'Username', 'Password', 'Company_ID', 'IS_admin', 'salt',
                       'last_ip', 'date_created', 'date_updated', 'remember_token',
                       'last_login']
    
    def __init__(self, oi=0, fn='', ln='', mn='', mc=0, e='', ca='', ma='',
                 usr='', pw='', ci=0, ia=0, ap='all', tp='', s='', ip='', dc='',
                 du='', rt='', ll=''):
        self.Operator_ID = oi
        self.First_name = fn
        self.Last_name = ln
        self.Mobile_num = mn
        self.Mobile_confirmed = mc
        self.Email = e
        self.Created_at = ca
        self.Modified_at = ma
        # Username
        self.Username = usr
        self.Password = pw
        self.Company_ID = ci
        # Whether the operator has admin privileges (if so, action and table permissions are automatically ignored)
        self.IS_admin = ia
        # String containing comma-separated list of action permissions (i.e. create, read, insert, update, or delete) 
        self.action_permissions = ap
        # String containing comma-separated list of tables this operator has access to
        self.table_permissions = tp
        self.salt = s
        self.last_ip = ip
        self.date_created = dc
        self.date_updated = du
        self.remember_token = rt
        self.last_login = ll

        # Used to get most up-to-date information about operator
        self.db = Database()

    # Populate respective operator attributes given username
    def populate_from_username(self, usr):
        # Find operator by credentials
        cur = self.db.query("SELECT * FROM operators WHERE Username = %s",
                            [usr])

        # Fetch one row with pertinent information
        r = cur.fetchone()

        # operator doesn't exist anymore or token is still invalid somehow
        if not r:
            raise HTTPException(status_code=500, detail="Operator does not exist")

        # Populate self with operator details
        for i, attr in enumerate(User.operator_fields):
            setattr(self, attr, r[i])
        
    # Retrieve a JWT token containing the operator's unique username to be indexed into db
    def get_token(self):
        # Retrieve secret signing key
        key = ServerConfig().get_config()['server_settings']['jwt_key']
        # Minutes until the JWT token expires
        expiry = ServerConfig().get_config()['server_settings']['token_expiry_minutes']

        # Negative expiry indicates no expiry time for the token (infinite token)
        if expiry < 0:
            return jwt.encode({
                        'sub': self.Username,
##                        'iad': self.is_admin,
##                        'acp': self.action_permissions,
##                        'tbp': self.table_permissions,
                        'iat': datetime.utcnow(),
                    }, key, algorithm='HS256')
        
        return jwt.encode({
            'sub': self.Username,
##            'iad': self.is_admin,
##            'acp': self.action_permissions,
##            'tbp': self.table_permissions,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=expiry)
        }, key, algorithm='HS256')

    # Validate a token and populate this user object with its data
    def validate_token(self, token):
        key = ServerConfig().get_config()['server_settings']['jwt_key']

        try:
            data = jwt.decode(token, key, algorithms=['HS256'])
        except Exception as e:
            if "expired" in str(e):
                raise HTTPException(status_code=400, detail="Token expired")
            else:
                raise HTTPException(status_code=400, detail="Error: " + str(e))

        self.populate_from_username(data['sub'])

        return data
