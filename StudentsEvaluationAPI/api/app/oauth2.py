"""
Module Name: Authentication

This module provides authentication functions and dependencies for the StudentsEvaluationAPI application.

Functions:
    - create_access_token: Creates an access token with the provided data.
    - verify_tok: Verifies the access token and returns token data.
    - get_current_user: Dependency function to get the current user from the access token.
    - get_admin_user: Dependency function to get the admin user from the access token.
    - get_teacher: Dependency function to get the teacher user from the access token.
    - get_guardian: Dependency function to get the guardian user from the access token.

Dependencies:
    - jose.JWTError: Exception class for JWT-related errors.
    - jose.jwt: Provides functions for encoding and decoding JSON Web Tokens (JWT).
    - datetime.datetime: Provides classes for working with dates and times.
    - datetime.timedelta: Represents a duration or difference between two dates or times.
    - .schemas: Module containing Pydantic schemas used in the application.
    - .database: Module providing database-related functions.
    - .models: Module containing database models.
    - fastapi.Depends: Dependency decorator for declaring dependencies.
    - fastapi.status: Provides HTTP status codes.
    - fastapi.HTTPException: Exception class for HTTP-specific exceptions.
    - .config.settings: Module containing application settings.
    - fastapi.security.OAuth2PasswordBearer: OAuth2 password bearer authentication scheme.

Global Constants:
    - SECRET_KEY: Secret key used for JWT token encoding and decoding.
    - ALGORITHM: Algorithm used for JWT token encoding and decoding.
    - ACCESS_TOKEN_EXPIRE_MINUTES: Number of minutes until the access token expires.
    - credentials_exception: HTTPException instance for unauthorized credentials.

Dependencies (continued):
    - oauth2_scheme: OAuth2 password bearer authentication scheme instance.

"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
# from .jwt_bearer import JWTBearer
from fastapi.security import OAuth2PasswordBearer

# jwt_bearer = JWTBearer()
# admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/administrator/sign-in")
# parent_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/administrator/sign-in")
# teacher_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/administrator/sign-in")
# student_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/student/sign-in")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token/sign-in")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_tok_expire_minutes)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def create_access_token(data: dict):
    """
    Create an access token with the provided data.

    Parameters:
        - data (dict): Data to be encoded in the access token.

    Returns:
        str: Encoded access token.
    """

    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})

    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_tok(token: str, credentialsException):
    """
    Verify the access token and extract token data.

    Parameters:
        - token (str): Access token to be verified.
        - credentialsException (HTTPException): Exception instance for unauthorized credentials.

    Returns:
        schemas.TokData: Token data extracted from the access token.

    Raises:
        HTTPException: If the access token is invalid or does not contain user_id.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id = payload.get("user_id")

        if not _id:
            raise credentialsException
        tok_data = schemas.TokData(id=_id)
    except JWTError:
        raise credentialsException
    return tok_data


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    """
    Dependency function to get the current user from the access token.

    Parameters:
        - token (str): Access token obtained from the request header.
        - db (Session): Database session dependency.

    Returns:
        models.Students: Current user retrieved from the database.

    Raises:
        HTTPException: If the access token is invalid, user is not found, or user is not authorized.
    """

    token = verify_tok(token, credentials_exception)
    user = db.query(models.Students).filter(models.Students.student_id == token.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to execute this action"
        )
    return user


def get_admin_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    """
    Dependency function to get the admin user from the access token.

    Parameters:
        - token (str): Access token obtained from the request header.
        - db (Session): Database session dependency.

    Returns:
        models.Admins: Admin user retrieved from the database.

    Raises:
        HTTPException: If the access token is invalid, user is not found, or user is not authorized.
    """

    token = verify_tok(token, credentials_exception)
    user = db.query(models.Admins).filter(models.Admins.admin_id == token.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to execute this action"
        )
    return user


def get_teacher(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    """
    Dependency function to get the teacher user from the access token.

    Parameters:
        - token (str): Access token obtained from the request header.
        - db (Session): Database session dependency.

    Returns:
        models.Teacher: Teacher user retrieved from the database.

    Raises:
        HTTPException: If the access token is invalid, user is not found, or user is not authorized.
    """

    token = verify_tok(token, credentials_exception)
    user = db.query(models.Teacher).filter(models.Teacher.teacher_id == token.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to execute this action"
        )
    return user


def get_guardian(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    """
    Dependency function to get the teacher user from the access token.

    Parameters:
        - token (str): Access token obtained from the request header.
        - db (Session): Database session dependency.

    Returns:
        models.Teacher: Teacher user retrieved from the database.

    Raises:
        HTTPException: If the access token is invalid, user is not found, or user is not authorized.
    """

    token = verify_tok(token, credentials_exception)
    user = db.query(models.Admins).filter(models.Guardians.email == token.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to execute this action"
        )
    return user
