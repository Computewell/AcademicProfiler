"""
Module Description

This module defines the API endpoints and functions for the administrator-related operations.
It provides functionalities for creating new administrators, retrieving teachers and students,
getting class information, retrieving class members, and accessing user profiles.

Dependencies:
- fastapi: FastAPI framework for building APIs
- sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library
- ..: Relative import for local modules
- schemas: Module containing data models (schemas) for API request/response bodies
- database: Module for managing the database connection
- models: Module containing ORM models for database tables
- utils: Module containing utility functions
- oauth2: Module for handling authentication and authorization

Exposed Endpoints:
- POST /admin/register: Create a new administrator
- GET /admin/teachers: Get all teachers
- GET /admin/students: Get all students
- GET /admin/get-classes: Get all class names
- GET /admin/{member_class}/members: Get class members
- GET /admin/user-profile/{member}/{member_class}/{name}: Get user profile

Tags:
- Administrators: Tag for the administrator-related endpoints

Prefix:
- /admin: Prefix for all administrator-related endpoints
"""

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2
from StudentsEvaluationAPI import __CLASSES__

router = APIRouter(tags=["Administrators"], prefix="/admin")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.Admin)
async def create_admin(
    user: schemas.AdministratorCreate, db: Session = Depends(database.get_db),
    role: str = Depends(oauth2.get_admin_user)
):
    """
    Create a new administrator.

    This function allows the creation of a new administrator in the system.

    Parameters:
        user (schemas.AdministratorCreate): The data of the new administrator.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        role (str, optional): The role of the user. Defaults to Depends(oauth2.get_admin_user).

    Returns:
        schemas.Admin: The newly created administrator.

    Raises:
        HTTPException: If there is an error in the registration process.
    """
    hashed_pwd = utils.hashed(user.password)
    user.password = hashed_pwd
    new_user = models.Admins(**user.dict())
    count = db.query(models.Admins).count()
    new_user.admin_id = utils.generate_registration_number("ADM", count + 1)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/teachers", response_model=list[schemas.Teacher])
async def get_all_teachers(
        db: Session = Depends(database.get_db),
        user: models.Admins = Depends(oauth2.get_admin_user)
):
    """
        Get all teachers.

        This function retrieves a list of all teachers in the system.

        Parameters:
            db (Session, optional): The database session. Defaults to Depends(database.get_db).
            user (models.Admins, optional): The admin user. Defaults to Depends(oauth2.get_admin_user).

        Returns:
            list[schemas.Teacher]: A list of all teachers.
    """
    return db.query(models.Teacher).all()


@router.get("/students", response_model=list[schemas.Students])
async def get_all_students(
    db: Session = Depends(database.get_db),
    user: models.Admins = Depends(oauth2.get_admin_user)
):
    """
    Get all students.

    This function retrieves a list of all students in the system.

    Parameters:
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        user (models.Admins, optional): The admin user. Defaults to Depends(oauth2.get_admin_user).

    Returns:
        list[schemas.Students]: A list of all students.
    """
    return db.query(models.Students).all()


@router.get("/get-classes", response_model=list[str])
async def get_all_classes(role: str = Depends(oauth2.get_admin_user)):
    """
    Get all class names.

    This function retrieves a list of all class names in the system.

    Parameters:
        role (str, optional): The role of the user. Defaults to Depends(oauth2.get_admin_user).

    Returns:
        list[str]: A list of all class names.
    """
    return __CLASSES__


@router.get("/{member_class}/members", response_model=list[str])
async def get_class_members(
    member_class: str, db: Session = Depends(database.get_db),
    role: str = Depends(oauth2.get_admin_user)
):
    """
    Get class members.

    This function retrieves a list of all members in a specific class.

    Parameters:
        member_class (str): The class name.
        db (Session, optional): The database session. Defaults to Depends(database.get_db).
        role (str, optional): The role of the user. Defaults to Depends(oauth2.get_admin_user).

    Returns:
        list[str]: A list of class members.
    """
    ret_val = []
    students = db.query(models.Students).filter(models.Students.student_class == member_class).all(),
    teachers = db.query(models.Teacher).filter(models.Teacher.class_taught == member_class).all()
    for teacher in teachers:
        if isinstance(teacher, list):
            for t in teacher:
                ret_val.append(t.name)
        else:
            ret_val.append(teacher.name)
    len_ret = len(ret_val)
    for student in students:
        if isinstance(student, list):
            for s in student:
                ret_val.append(s.lastname + " " + s.firstname)
        else:
            ret_val.append(student.lastname + " " + student.firstname)

    sub_ret_teacher = ret_val[:len_ret]
    sub_ret_student = ret_val[len_ret:]
    sub_ret_teacher = sorted(sub_ret_teacher)
    sub_ret_student = sorted(sub_ret_student)
    ret_val = sub_ret_teacher + sub_ret_student

    return ret_val


@router.get("/user-profile/{member}/{member_class}/{name}", response_model=schemas.Member)
async def get_user_profile(
    member_class: str, member: str, name: str,
    user: models.Admins = Depends(oauth2.get_admin_user),
    db: Session = Depends(database.get_db)
):
    """
    Get user profile.

    This function retrieves the profile information of a user (student or teacher).

    Parameters:
        member_class (str): The class name.
        member (str): The member type ("student" or "teacher").
        name (str): The name of the member.
        user (models.Admins, optional): The admin user. Defaults to Depends(oauth2.get_admin_user).
        db (Session, optional): The database session. Defaults to Depends(database.get_db).

    Returns:
        schemas.Member: The profile information of the user.
    """
    ret_val = {}
    if member.strip() == "student":
        ret_val["Designation"] = "Student"
        students = db.query(models.Students).filter(
            (models.Students.student_class == member_class) and (models.Students.lastname == name.strip().split(" ")[0])
        ).first()

        if not students:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{member} with name {name} not found")

        for key, value in students.__dict__.items():
            ret_val[key] = value

    elif member.strip() == "teacher":
        ret_val["Designation"] = "Teacher"
        teachers = db.query(models.Teacher).filter(
            (models.Teacher.class_taught == member_class) and (models.Teacher.name == name.strip())
        ).first()

        if not teachers:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{member} with name {name} not found")

        for k, v in teachers.__dict__.items():
            ret_val[k] = v

    return ret_val
