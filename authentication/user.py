import jwt
from server.server_config import ServerConfig
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel
import json

# This class contains all the necessary information to describe an operator, or user
# The information can be encoded into a JWT token
# The JWT token can also be decoded back to a User object
class User():
    
    def __init__(self, usr='', is_admin=False, ap='', tp=''):
        # Username
        self.username = usr
        # Whether the operator has admin privileges (if so, action and table permissions are automatically ignored)
        self.is_admin = is_admin
        # String containing comma-separated list of action permissions (i.e. create, read, insert, update, or delete) 
        self.action_permissions = ap
        # String containing comma-separated list of tables this operator has access to
        self.table_permissions = tp

    # Retrieve a JWT token containing the operator's data
    def get_token(self):
        # Retrieve secret signing key
        key = ServerConfig().get_config()['server_settings']['jwt_key']
        # Minutes until the JWT token expires
        expiry = ServerConfig().get_config()['server_settings']['token_expiry_minutes']

        # Negative expiry indicates no expiry time for the token (infinite token)
        if expiry < 0:
            return jwt.encode({
                        'sub': self.username,
                        'iad': self.is_admin,
                        'acp': self.action_permissions,
                        'tbp': self.table_permissions,
                        'iat': datetime.utcnow(),
                    }, key, algorithm='HS256')
        
        return jwt.encode({
            'sub': self.username,
            'iad': self.is_admin,
            'acp': self.action_permissions,
            'tbp': self.table_permissions,
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

        self.username = data['sub']
        self.is_admin = data['iad']
        self.action_permissions = data['acp']
        self.table_permissions = data['tbp']

        return data
