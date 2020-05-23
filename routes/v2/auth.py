from server.schemas import Token, Detail
from authentication.login import Login
from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
login = Login()

# Following route is for authenticating the user and returning their respective JWT token
@router.post(
    '/get_token',
    response_model=Token,
    response_description="Returns user private access token. Make sure to keep the token secret.",
    summary="Authenticate API user",
    description="""Authenticate an API user and return a token that will be passed in the
                    authorization header for subsequent requests""",
    responses = {400: {"model": Detail}, 500: {"model": Detail}}
)

# Username is securely handled using OAuth2
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
  # Validate credentials and return the user's token
  r = login.validate_user(form_data.username, form_data.password)
  if r and r["status"] != "success":
    raise HTTPException(status_code=400, detail=r["details"])
  return {"access_token": r["user"].get_token(), "token_type": "bearer"}
