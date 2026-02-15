# APIRouter Class will allow to route calls from our main file to auth file

from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from starlette import status
from passlib.context import CryptContext

# Using the Bearer token fro security, we are telling FastAPI to check the header for bearer JWT token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import jwt, JWTError


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '9cf52cdb844c9299ad4d91792d2821245f83004231028efd2dbf10a468403d39'

ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Creating new dependecy on which API endpoint would rely on
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
# tokenUrl is a URL which client will send to our FastAPI application to check the token


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user_statement = select(Users).where(Users.username == username)
    user_model_data = db.scalars(user_statement).first()
    if not user_model_data:
        return False
    
    if not bcrypt_context.verify(password, user_model_data.hashed_password):
        return False
    
    return user_model_data

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }

    expires = datetime.now(timezone.utc) + expires_delta

    encode.update({
        'exp': expires
    })

    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get('sub')
        user_id: str | None = payload.get('id')
        user_role: str | None = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        return {'username': username, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)

    db.commit()

    # Without this refresh, the return would be a null object. This is because SQLAlchemy expires' 
    # the Object's (create_user_model) state, thus making it point to NULL immediately after calling
    # 'db.commit()'

    # db.refresh(create_user_model) # Do not need to send it back in real-world applications

    return create_user_model

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

