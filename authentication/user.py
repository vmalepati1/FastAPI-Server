import jwt
from server.server_config import ServerConfig
from datetime import datetime, timedelta
from fastapi import HTTPException

class User:
    
    def __init__(self, usr='', is_admin=False, ap='', tp=''):
        self.username = usr
        self.is_admin = is_admin
        self.action_permissions = ap
        self.table_permissions = tp

    def get_token(self):
        key = ServerConfig().get_config()['server_settings']['jwt_key']
        expiry = ServerConfig().get_config()['server_settings']['token_expiry_minutes']
        
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
