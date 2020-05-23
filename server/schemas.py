from pydantic import BaseModel
from typing import Optional, Any
from typing import List
import datetime

# The following are schema structures returned by the routed endpoints

class Token(BaseModel):
    access_token: str
    token_type: str

class Detail(BaseModel):
    detail: str

class Querysimo(BaseModel):
    rows: List[dict]

class QueryResult(BaseModel):
    rows: tuple

# Uses Any in case some fields are null
class User(BaseModel):
    Operator_ID: int
    First_name: Optional[str]
    Last_name: Optional[str]
    Mobile_num: Optional[str]
    Mobile_confirmed: Optional[int]
    Email: Optional[str]
    Created_at: Optional[datetime.datetime]
    Modified_at: Optional[datetime.datetime]
    Username: Optional[str]
    Password: Optional[str]
    Company_ID: Optional[int]
    IS_admin: Optional[int]
    salt: Optional[str]
    last_ip: Optional[str]
    date_created: Optional[datetime.datetime]
    date_updated: Optional[datetime.datetime]
    remember_token: Optional[str]
    last_login: Optional[datetime.datetime]
