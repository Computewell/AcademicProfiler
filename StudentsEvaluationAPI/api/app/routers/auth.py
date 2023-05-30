"""
Module Description

This module defines the authentication endpoints for user login. It provides functionality for
verifying user credentials and generating access tokens.

Dependencies:
- fastapi: FastAPI framework for building APIs
- Response: FastAPI Response class for handling HTTP responses
- HTTPException: FastAPI HTTPException class for raising exceptions with status codes
- status: HTTP status codes module for specifying response status codes
- Depends: FastAPI Dependency class for handling dependencies
- models: Module containing ORM models for database tables
- schemas: Module containing data models (schemas) for API request/response bodies
- utils: Module containing utility functions
- oauth2: Module for handling OAuth2 authentication

Exposed Endpoints:
- POST /auth/token/sign-in: User login and access token generation

Tags:
- Authentications: Tag for the authentication-related endpoints

Prefix:
- /auth: Prefix for all authentication-related endpoints
"""

from fastapi import APIRouter, Response, HTTPException, status, Depends
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentications"], prefix="/auth")


@router.post("/token/sign-in", response_model=schemas.UserLogin)
async def user_login(
    res: Response,
    usr_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    User Login

    Authenticates the user based on the provided credentials and generates an access token.

    Parameters:
    - res (Response): FastAPI Response object for setting cookies and returning the response.
    - usr_credentials (OAuth2PasswordRequestForm): Form containing user credentials (username and password).
    - db (Session): SQLAlchemy Session object for database operations.

    Returns:
    - dict: Dictionary containing user information and access token.

    Raises:
    - HTTPException(403): If the login credentials are invalid.

    """
    res_role = "parent"
    if usr_credentials.username.startswith("ADM"):
        res_role = "admin"
        user = db.query(models.Admins).filter(models.Admins.admin_id == usr_credentials.username).first()
        if not user or not utils.verify(usr_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")
        access_tok = oauth2.create_access_token(data={"user_id": user.admin_id})
    elif usr_credentials.username.startswith("STU"):
        res_role = "student"
        user = db.query(models.Students).filter(models.Students.student_id == usr_credentials.username).first()
        if not user or not utils.verify(usr_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")
        access_tok = oauth2.create_access_token(data={"user_id": user.student_id})
    elif usr_credentials.username.startswith("TCH"):
        res_role = "teacher"
        user = db.query(models.Teacher).filter(models.Teacher.teacher_id == usr_credentials.username).first()
        if not user or not utils.verify(usr_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")
        access_tok = oauth2.create_access_token(data={"user_id": user.teacher_id})
    else:
        user = db.query(models.Guardians).filter(models.Guardians.email == usr_credentials.username).first()
        if not user or not utils.verify(usr_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")
        access_tok = oauth2.create_access_token(data={"user_id": user.email})

    res.set_cookie(key="token", value=access_tok)
    return {
        "name": user.name,
        "access_token": access_tok,
        "token_type": "bearer",
        "id": user.id,
        "role": res_role
    }
#
# @router.post("/students/sign-in", response_model=schemas.StudentLogin)
# async def student_login(
#         res: Response,
#         usr_credentials: OAuth2PasswordRequestForm = Depends(),
#         db: Session = Depends(get_db)
# ):
#     user = db.query(models.Students).filter(models.Students.student_id == usr_credentials.username).first()
#     if not user or not utils.verify(usr_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid login credentials")
#
#     access_tok = oauth2.create_access_token(data={"user_id": user.student_id})
#     res.set_cookie(key="token", value=access_tok)
#     return {
#         "name": user.name,
#         "access_token": access_tok,
#         "token_type": "bearer",
#         "id": user.student_id
#     }
#
#
# @router.post("/administrator/sign-in", response_model=schemas.AdminLogin)
# async def admin_login(
#         res: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     user = db.query(models.Admins).filter(models.Admins.email == request.username).first()
#
#     if not user or not utils.verify(request.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Login Credentials")
#
#     access_token = oauth2.create_access_token(data={"user_id": user.email})
#     res.set_cookie(key="token", value=access_token)
#     return {
#         "name": user.name,
#         "access_token": access_token,
#         "token_type": "bearer",
#         "email": user.email
#     }
#
#
# @router.post("/guardian/sign-in", response_model=schemas.StudentLogin)
# async def guardian_login(
#         res: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     user = db.query(models.Guardians).filter(models.Guardians.email == request.username).first()
#
#     if not user or not utils.verify(request.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Login Credentials")
#
#     access_token = oauth2.create_access_token(data={"user_id": user.id})
#     res.set_cookie(key="token", value=access_token)
#     return {
#         "name": user.name,
#         "access_token": access_token,
#         "token_type": "bearer",
#         "id": user.id
#     }
#
#
# @router.post("/teacher/sign-in", response_model=schemas.StudentLogin)
# async def teacher_login(
#         res: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     user = db.query(models.Teacher).filter(models.Teacher.email == request.username).first()
#
#     if not user or not utils.verify(request.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Login Credentials")
#
#     access_token = oauth2.create_access_token(data={"user_id": user.name})
#     res.set_cookie(key="token", value=access_token)
#     return {
#         "name": user.name,
#         "access_token": access_token,
#         "token_type": "bearer",
#         "id": user.id
#     }
