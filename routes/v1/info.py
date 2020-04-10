from server.schemas import Detail
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
import authentication.user
import server.schemas

# Following route returns general information about the server and its users
router = APIRouter()

# Enables us to retrieve token passed through the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/get_token')

@router.get(
    '/get_info',
    response_model=server.schemas.User,
    response_description="Returns information about user",
    summary="Retrieve information regarding user given their token",
    description="Retrieve information regarding a user (such as permissions) given their token",
    responses = {200: {"model": Detail}, 401: {"model": Detail}, 403: {"model": Detail}}
)

async def get_info(token: str = Depends(oauth2_scheme)):
    user = authentication.user.User()
    user.validate_token(token)
    # Convert user object to dict and return
    return vars(user)
