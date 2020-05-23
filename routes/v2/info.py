from server.schemas import Detail
from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
import authentication.user
import server.schemas
from database.permissions import Permissions

# Following route returns general information about the server and its users
router = APIRouter()
perms = Permissions()

# Enables us to retrieve token passed through the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v2/auth/get_token')

@router.get(
    '/get_info',
    response_model=server.schemas.User,
    response_description="Returns information about user",
    summary="Retrieve information regarding either the current user (given their token) or another user (specifying other_username)",
    description="Retrieve information regarding a user (such as permissions)",
    responses = {200: {"model": Detail}, 401: {"model": Detail}, 403: {"model": Detail}, 500: {"model": Detail}}
)

async def get_info(
    other_username: str = Query(
        None,
        description="Username of another user to return information about (only for admins)"
    ),
    token: str = Depends(oauth2_scheme)
):
    user = authentication.user.User()
    user.validate_token(token)

    if other_username:
        # Validate access to other user
        perms.validate_operator_access(user, other_username)
        other_user = authentication.user.User()
        other_user.populate_from_username(other_username)
        # Return other user data
        return vars(other_user)
    
    # Convert current user object to dict and return
    return vars(user)
