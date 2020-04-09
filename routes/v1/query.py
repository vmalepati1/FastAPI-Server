from server.schemas import Token, Detail, QueryResult
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from authentication.user import User
from database.permissions import Permissions
from database.db import Database
from database.actions import *

router = APIRouter()
perms = Permissions()
db = Database('api_db')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/get_token')

@router.post(
    '/create',
    response_model=Detail,
    response_description="Returns status of request",
    summary="Create a table in the database",
    responses = {200: {"model": Detail}, 400: {"model": Detail}, 403: {"model": Detail}}
)

async def create(table_name : str, field_defs : str, token: str = Depends(oauth2_scheme)):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, CREATE)

    try:
        db.query("CREATE TABLE {0} ({1});"
                 .format(table_name, field_defs))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
        
    return {"detail": "Success"}

@router.get(
    '/read',
    response_model=QueryResult,
    response_description="Returns the query result as a list of tuples",
    summary="Read record from the database",
    description="Read a record from the database and return all rows as a list of tuples",
    responses = {200: {"model": Detail}, 400: {"model": Detail}, 403: {"model": Detail}}
)

async def read(what_to_select : str, which_table : str, conditions_to_satisfy : str = None, token: str = Depends(oauth2_scheme)):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, READ, which_table)

    try:
        if not conditions_to_satisfy:
            cur = db.query("SELECT {0} FROM {1};"
                     .format(what_to_select, which_table))
        else:
            cur = db.query("SELECT {0} FROM {1} WHERE {2};"
                     .format(what_to_select, which_table, conditions_to_satisfy))

        return {"rows": cur.fetchall()}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))

@router.post(
    '/insert',
    response_model=Detail,
    response_description="Returns status of request",
    summary="Insert record into database table",
    responses = {200: {"model": Detail}, 400: {"model": Detail}, 403: {"model": Detail}}
)

async def insert(table_name : str, value_names : str, column_names : str = None, token: str = Depends(oauth2_scheme)):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, INSERT, table_name)

    try:
        if not column_names:
            db.query("INSERT INTO {0} VALUES ({1});"
                 .format(table_name, value_names))
        else:
            db.query("INSERT INTO {0} ({1}) VALUES ({2});"
                 .format(table_name, column_names, value_names))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
        
    return {"detail": "Success"}
