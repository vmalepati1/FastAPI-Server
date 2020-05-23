from server.schemas import Token, Detail, QueryResult, Querysimo
from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from authentication.user import User
from database.permissions import Permissions
from database.db import Database
from database.actions import *
import bcrypt
import time
import datetime
import re

# Following routes are for performing database query requests
router = APIRouter()
perms = Permissions()
# Establish database for the query API
db = Database()

# Enables us to retrieve token passed through the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v2/auth/get_token")

# Create a table
@router.post(
    "/create",
    response_model=Detail,
    response_description="Returns status of request",
    summary="Create a table in the database",
    responses={
        200: {"model": Detail},
        400: {"model": Detail},
        401: {"model": Detail},
        403: {"model": Detail},
        500: {"model": Detail}
    },
)
async def create(
    table_name: str = Query(..., description="Table name in database, eg `categories`"),
    field_defs: str = Query(
        ...,
        description="List of column names followed by their types, eg `Category_ID int(11), Category_Name varchar(500)`",
    ),
    token: str = Depends(oauth2_scheme),
):
    # Validate token and retrieve user data
    user = User()
    user.validate_token(token)
    perms.validate_action(user, CREATE)

    # Perform SQL query
    try:
        db.query("CREATE TABLE {0} ({1});".format(table_name, field_defs))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
    return {"detail": "Success"}


# Read a record
@router.get(
    "/read",
    response_model=Querysimo,
    response_description="Returns the query result as a list of tuples",
    summary="Read record from the database",
    description="Read a record from the database and return all rows as a list of tuples",
    responses={
        200: {"model": Detail},
        400: {"model": Detail},
        401: {"model": Detail},
        403: {"model": Detail},
        500: {"model": Detail}
    },
)
async def read(
    what_to_select: str = Query(
        ...,
        description="List of columns, or * to indicate all columns, eg `Category_Name, ICON_URL`",
    ),
    which_table: str = Query(
        ..., description="Name of table to retrieve data from, eg `categories`"
    ),
    conditions_to_satisfy: str = Query(
        None,
        description="If present, specifies one or more conditions that records must satisfy for retrieval, eg `Category_ID = 1`",
    ),
    token: str = Depends(oauth2_scheme),
):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, READ, which_table)

    try:
        if not conditions_to_satisfy:
            cur = db.query("SELECT {0} FROM {1};".format(what_to_select, which_table))
        else:
            cur = db.query(
                "SELECT {0} FROM {1} WHERE {2};".format(
                    what_to_select, which_table, conditions_to_satisfy
                )
            )
        return {"rows": cur.fetchall()}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))


@router.post(
    "/insert",
    response_model=Detail,
    response_description="Returns status of request",
    summary="Insert record into database table",
    responses={
        200: {"model": Detail},
        400: {"model": Detail},
        401: {"model": Detail},
        403: {"model": Detail},
        500: {"model": Detail}
    },
)

# Insert a record
async def insert(
    table_name: str = Query(
        ..., description="Name of table to insert record into, eg `categories`"
    ),
    values: str = Query(
        ...,
        description="List of field values for the record with each surrounded by single quotes, eg `'1', 'IT', 'google.com'`",
    ),
    column_names: str = Query(
        None,
        description="""List of column names that you are specifying values for in the record, eg `Category_ID, Category_Name, ICON_URL`. If you
                        are adding values for all the columns of the table, you do not need to specify this parameter""",
    ),
    token: str = Depends(oauth2_scheme),
):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, INSERT, table_name)
    try:
        if not column_names:
            db.query("INSERT INTO {0} VALUES ({1});".format(table_name, values))
        else:
            if "Password" in column_names:
                colonnelista = column_names.split(",")
                valorilista = values.split(",")
                indice = colonnelista.index("Password")
                passattuale = valorilista[indice]
                salt = bcrypt.gensalt()
                passnuova = bcrypt.hashpw(passattuale.encode(), salt).decode("utf-8")
                valorilista[indice] = passnuova
                valoristringa = '","'.join(valorilista)
                valoroni = '"' + valoristringa + '"'
                values = valoroni
            db.query(
                "INSERT INTO {0} ({1}) VALUES ({2});".format(
                    table_name, column_names, values
                )
            )
        cur = db.query("SHOW columns FROM {0};".format(table_name))
        fields = [c[0] for c in cur.fetchall()]

        cur = db.query(
            "SHOW KEYS FROM {0} WHERE Key_name = 'PRIMARY';".format(table_name)
        )
        dat = cur.fetchone()
        pk_index = dat[3] - 1
        pk = dat[4]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        # Inserting a record requires management of the "Created_at" and "Modified_at" fields,
        # if they exist. Find record by primary key and then update with current time stamp.
        if "Created_at" in fields:
            db.query(
                "UPDATE {0} SET Created_at = '{1}' WHERE {2} = {3};".format(
                    table_name, timestamp, pk, re.split(r"[,\s]\s*", values)[pk_index]
                )
            )
        if "Modified_at" in fields:
            db.query(
                "UPDATE {0} SET Modified_at = '{1}' WHERE {2} = {3};".format(
                    table_name, timestamp, pk, re.split(r"[,\s]\s*", values)[pk_index]
                )
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
    return {"detail": "Success"}


# Update a record
@router.put(
    "/update",
    response_model=Detail,
    response_description="Returns status of request",
    summary="Update record in the database",
    responses={
        200: {"model": Detail},
        400: {"model": Detail},
        401: {"model": Detail},
        403: {"model": Detail},
        500: {"model": Detail}
    },
)
async def update(
    table_name: str = Query(
        ...,
        description="Name of table in which record will be updated, eg `categories`",
    ),
    set_statements: str = Query(
        ...,
        description="List of columns to modify and their respective values (surrounded by single quotes), eg `Category_Name = 'IT', ICON_URL = 'google.com'`",
    ),
    where_condition: str = Query(
        None,
        description="Specifies the conditions that identify which records to update, eg `Category_ID = 1`. If omitted, all records are updated",
    ),
    token: str = Depends(oauth2_scheme),
):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, UPDATE, table_name)

    try:
        cur = db.query("SHOW columns FROM {0};".format(table_name))
        fields = [c[0] for c in cur.fetchall()]

        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        if not where_condition:
            # Update Modified_at with current timestamp for all records
            if "Modified_at" in fields:
                db.query(
                    "UPDATE {0} SET Modified_at = '{1}';".format(table_name, timestamp)
                )
            db.query("UPDATE {0} SET {1};".format(table_name, set_statements))
        else:
            # Update Modified_at with current timestamp for just the changed record
            if "Modified_at" in fields:
                db.query(
                    "UPDATE {0} SET Modified_at = '{1}' WHERE {2};".format(
                        table_name, timestamp, where_condition
                    )
                )
            db.query(
                "UPDATE {0} SET {1} WHERE {2};".format(
                    table_name, set_statements, where_condition
                )
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
    return {"detail": "Success"}


# Delete a record
@router.delete(
    "/delete",
    response_model=Detail,
    response_description="Returns status of request",
    summary="Delete record from the database",
    responses={
        200: {"model": Detail},
        400: {"model": Detail},
        401: {"model": Detail},
        403: {"model": Detail},
        500: {"model": Detail}
    },
)
async def delete(
    table_name: str = Query(
        ...,
        description="Name of table in which record will be deleted, eg `categories`",
    ),
    where_condition: str = Query(
        None,
        description="Specifies which record or records should be deleted, eg `Category_Name = 'IT'`. If omitted, all records will be deleted!",
    ),
    token: str = Depends(oauth2_scheme),
):
    user = User()
    user.validate_token(token)
    perms.validate_action(user, DELETE, table_name)

    try:
        if not where_condition:
            db.query("DELETE FROM {0};".format(table_name, where_condition))
        else:
            db.query("DELETE FROM {0} WHERE {1};".format(table_name, where_condition))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error: " + str(e))
    return {"detail": "Success"}

