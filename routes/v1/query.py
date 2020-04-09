from server.schemas import Token, Detail, QueryResult
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from authentication.user import User
from database.permissions import Permissions
from database.db import Database
from database.actions import *
import time
import datetime
import re

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

async def insert(table_name : str, values : str, column_names : str = None, token: str = Depends(oauth2_scheme)):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, INSERT, table_name)

    try:
        if not column_names:
            db.query("INSERT INTO {0} VALUES ({1});"
                 .format(table_name, values))
        else:
            db.query("INSERT INTO {0} ({1}) VALUES ({2});"
                 .format(table_name, column_names, values))

        cur = db.query("SHOW columns FROM {0};"
                 .format(table_name))
        
        fields = [c[0] for c in cur.fetchall()]

        pk = fields[0]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        if 'Created_at' in fields:
            db.query("UPDATE {0} SET Created_at = '{1}' WHERE {2} = {3};"
                 .format(table_name, timestamp, pk, values[0]))
            
        if 'Modified_at' in fields:
            db.query("UPDATE {0} SET Modified_at = '{1}' WHERE {2} = {3};"
                 .format(table_name, timestamp, pk, values[0]))

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))

    return {"detail": "Success"}

@router.put(
    '/update',
    response_model=Detail,
    response_description="Returns status of request",
    summary="Update record in the database. Not specifying the where clause will update all records.",
    responses = {200: {"model": Detail}, 400: {"model": Detail}, 403: {"model": Detail}}
)

async def update(table_name : str, set_statements : str, where_condition : str = None, token: str = Depends(oauth2_scheme)):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, UPDATE, table_name)

    try:
        cur = db.query("SHOW columns FROM {0};"
         .format(table_name))
    
        fields = [c[0] for c in cur.fetchall()]

        pk = fields[0]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        if not where_condition:
            if 'Modified_at' in fields:
                db.query("UPDATE {0} SET Modified_at = '{1}';"
                     .format(table_name, timestamp))
                
            db.query("UPDATE {0} SET {1};"
                 .format(table_name, set_statements))
        else:
            if 'Modified_at' in fields:
                pk_val = re.split(r'[,\s]\s*', where_condition)[2]

                db.query("UPDATE {0} SET Modified_at = '{1}' WHERE {2} = {3};"
                     .format(table_name, timestamp, pk, pk_val))
                
            db.query("UPDATE {0} SET {1} WHERE {2};"
                 .format(table_name, set_statements, where_condition))

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
        
    return {"detail": "Success"}

@router.delete(
    '/delete',
    response_model=Detail,
    response_description="Returns status of request",
    summary="Delete record from the database. Not specifying the where clause will delete all records.",
    responses = {200: {"model": Detail}, 400: {"model": Detail}, 403: {"model": Detail}}
)

async def delete(table_name : str, where_condition : str = None, token: str = Depends(oauth2_scheme)):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, DELETE, table_name)

    try:
        if not where_condition:
            db.query("DELETE FROM {0};"
                 .format(table_name, where_condition))
        else:
            db.query("DELETE FROM {0} WHERE {1};"
                 .format(table_name, where_condition))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
        
    return {"detail": "Success"}
