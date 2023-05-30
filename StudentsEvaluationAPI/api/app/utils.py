"""
Module Name: AuthenticationUtils

This module provides utility functions for authentication and file validation in a FastAPI application.

Functions:
    - hashed(password: str) -> str: Hashes the provided password using bcrypt encryption.
    - verify(attempted_password, usr_password) -> bool: Verifies if a password matches a hashed user password.
    - get_student_with_id(user_id, db: Session) -> models.Students: Retrieves a student from the database by ID.
    - validate_file(file: UploadFile, max_size: int, mime_types: list) -> UploadFile: Validates an uploaded file.
    - generate_suffix(val) -> str: Generates a random 3-digit suffix based on a provided value.
    - generate_registration_number(role, val: int) -> str: Generates a complete matriculation number based on role and value.

Dependencies:
    - fastapi.Depends: Dependency injection mechanism for FastAPI.
    - fastapi.HTTPException: Exception class for HTTP-specific exceptions.
    - fastapi.status: Provides HTTP status codes.
    - fastapi.UploadFile: Represents an uploaded file in FastAPI.
    - passlib.context.CryptContext: Password hashing and verification utility.
    - sqlalchemy.orm.Session: Database session object.
    - StudentsEvaluationAPI.api.app.database: Database related utilities.
    - StudentsEvaluationAPI.api.app.models: Data models for the application.
    - uuid: Generates universally unique identifiers (UUIDs).
    - datetime.datetime: Provides classes for working with dates and times.
"""


from fastapi import Depends, HTTPException, status, UploadFile
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from StudentsEvaluationAPI.api.app import database, models
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed(password: str):
    """Hashes the provided password using the configured encryption algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify(attempted_password, usr_password):
    """Verifies if the attempted password matches the provided user password.

    Args:
        attempted_password: The password to be verified.
        usr_password: The user's stored hashed password.

    Returns:
        bool: True if the password is verified, False otherwise.
    """
    return pwd_context.verify(attempted_password, usr_password)


def get_student_with_id(user_id, db: Session = Depends(database.get_db)):
    """Retrieves a student with the specified user ID from the database.

    Args:
        user_id: The ID of the student to retrieve.
        db (Session): The database session dependency.

    Raises:
        HTTPException: If the student with the specified ID is not found.

    Returns:
        models.Students: The retrieved student.
    """
    found_user = db.query(models.Students).filter(models.Students.id == user_id)
    is_found = found_user.first()
    if not is_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return is_found


async def validate_file(file: UploadFile, max_size: int = None, mime_types: list = None):
    """Validates the uploaded file by checking its size and MIME types.

    Args:
        file (UploadFile): The file to be validated.
        max_size (int, optional): The maximum allowed file size in bytes. Defaults to None.
        mime_types (list, optional): The allowed MIME types (content types) for the file. Defaults to None.

    Raises:
        HTTPException: If the file does not meet the validation criteria.

    Returns:
        UploadFile: The validated file.
    """
    if mime_types and file.content_type not in mime_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only upload image for party logo"
        )

    if max_size:
        size = await file.read()
        if len(size) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size is too big. Limit is 10mb"
            )
        await file.seek(0)
    return file


def generate_suffix(val):
    """Generates a random 3-digit suffix based on the provided value.

    Args:
        val: The value used to generate the suffix.

    Returns:
        str: The generated suffix.
    """
    suffix = str(val).zfill(3)
    return suffix


def generate_registration_number(role, val: int):
    """Generates a complete matriculation number based on the provided role and value.

    Args:
        role (str): The role of the user (STU, ADM, TCH).
        val (int): The value used to generate the suffix.

    Returns:
        str: The generated matriculation number.
    """
    suffix = generate_suffix(val)
    year = datetime.now().year % 100
    if role == "STU":
        return f"STU{year}{suffix}"
    elif role == "ADM":
        return f"ADM{suffix}"
    elif role == "TCH":
        return f"TCH{year}{suffix}"
