from pydantic import BaseModel

# The following are schema structures returned by the routed endpoints

class Token(BaseModel):
    access_token: str
    token_type: str

class Detail(BaseModel):
    detail: str

class QueryResult(BaseModel):
    rows: tuple
