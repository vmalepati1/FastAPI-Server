from pydantic import BaseModel
from typing import Any

# The following are schema structures returned by the routed endpoints

class Token(BaseModel):
    access_token: str
    token_type: str

class Detail(BaseModel):
    detail: str


class Querysimo(BaseModel):
    rows: dict

class QueryResult(BaseModel):
    rows: tuple

# Uses Any in case some fields are null
class User(BaseModel):
    Operator_ID: int
    First_name: Any
    Last_name: Any
    Mobile_num: Any
    Mobile_confirmed: Any
    Email: Any
    Created_at: Any
    Modified_at: Any
    Username: Any
    Password: Any
    Company_ID: Any
    IS_admin: Any
    salt: Any
    last_ip: Any
    date_created: Any
    date_updated: Any
    remember_token: Any
    last_login: Any
