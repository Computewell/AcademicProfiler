"""
Module Name: Schemas

This module defines the data schemas used in the StudentsEvaluationAPI application.

Classes:
    - Subject: Custom string class representing a subject. Validates against a list of valid subjects.
    - Term: Custom string class representing a term. Validates against a list of valid terms.
    - Classes: Custom string class representing a student class. Validates against a list of valid classes.
    - Results: Data schema representing the results of a student's subject.
    - PostGrade: Data schema representing the grades to be posted for a student.
    - Session: Data schema representing a session and term.
    - StudentsBase: Base data schema representing common fields for student data.
    - StudentsCreate: Data schema representing the creation of a student.
    - StudentsUpdate: Data schema representing the update of student data.
    - Students: Data schema representing a student.
    - StudentSubject: Data schema representing a student's subject.
    - Member: Data schema representing a member (teacher, admin, etc.).
    - TeacherBase: Base data schema representing common fields for teacher data.
    - TeacherCreate: Data schema representing the creation of a teacher.
    - TeacherUpdate: Data schema representing the update of teacher data.
    - Teacher: Data schema representing a teacher.
    - UpdatePassword: Data schema representing the update of a user's password.
    - AdminBase: Base data schema representing common fields for administrator data.
    - AdministratorCreate: Data schema representing the creation of an administrator.
    - AdministratorUpdate: Data schema representing the update of administrator data.
    - Admin: Data schema representing an administrator.
    - GuardianBase: Base data schema representing common fields for guardian data.
    - GuardianCreate: Data schema representing the creation of a guardian.
    - Guardian: Data schema representing a guardian.
    - Parent: Data schema representing a parent.
    - LoginBase: Base data schema representing common fields for login data.
    - AdminLogin: Data schema representing the login of an admin.
    - StudentLogin: Data schema representing the login of a student.
    - UserLogin: Data schema representing the login of a user.
    - TokData: Data schema representing token data.
    - NewsBase: Base data schema representing common fields for news data.
    - PostNews: Data schema representing the creation of news.
    - UpdateNews: Data schema representing the update of news data.
    - News: Data schema representing news.

Dependencies:
    - datetime.datetime: Provides classes for working with dates and times.
    - typing.Optional: Optional type hints.
    - typing.List: List type hints.
    - pydantic.BaseSchema: Base class for data schemas with validation and serialization capabilities.
    - pydantic.EmailStr: Data schema representing a validated email string.
    - pydantic.validator: Decorator for adding validation functions to schema fields.
    - StudentsEvaluationAPI.__SUBJECT_LISTS__: List of valid subjects.
    - StudentsEvaluationAPI.__CLASSES__: List of valid classes.
    - StudentsEvaluationAPI.__TERM__: List of valid terms.
    - fastapi.HTTPException: Exception class for HTTP-specific exceptions.
    - fastapi.status: Provides HTTP status codes.
"""


from datetime import datetime, date
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, validator
from StudentsEvaluationAPI import __SUBJECT_LISTS__, __CLASSES__, __TERM__
from fastapi import HTTPException, status


class Subject(str):
    __subject_list__ = __SUBJECT_LISTS__

    def __new__(cls, value):
        if value not in cls.__subject_list__:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{value} is not a valid subject"
            )
        return str.__new__(cls, value)


class Term(str):
    __term_list__ = __TERM__

    def __new__(cls, value):
        if value not in cls.__term_list__:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{value} is not a valid term"
            )
        return str.__new__(cls, value)


class Classes(str):
    __classes_list__ = __CLASSES__

    def __new__(cls, value):
        if value not in cls.__classes_list__:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{value} is not a valid student class"
            )
        return str.__new__(cls, value)


class Results(BaseModel):
    subject: str
    c_a_score: Optional[float] = 0.0
    exam_score: Optional[float] = 0.0

    class Config:
        orm_mode = True


class PostGrade(BaseModel):
    student_id: str
    c_a_score: Optional[float] = 0.0
    exam_score: Optional[float] = 0.0


class Session(BaseModel):
    session: str
    term: Term


class StudentsBase(BaseModel):
    firstname: str
    lastname: str
    middlename: Optional[str]
    email: EmailStr


class StudentsCreate(StudentsBase):
    password: str
    gender: str
    address: str
    student_class: Classes
    department: Optional[str]


class StudentsUpdate(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    middlename: Optional[str]
    email: Optional[EmailStr]
    gender: Optional[str]
    address: Optional[str]
    student_class: Optional[Classes]


class Students(StudentsBase):
    id: int
    student_id: str
    student_class: Classes
    department: Optional[str]

    class Config:
        orm_mode = True


class StudentSubject(BaseModel):
    lastname: str
    firstname: str
    student_id: str

    class Config:
        orm_mode = True


class Member(BaseModel):
    id: int
    Designation: str
    title: Optional[str] = ""
    name: Optional[str] = ""
    lastname: Optional[str] = ""
    firstname: Optional[str] = ""
    middlename: Optional[str] = ""
    gender: str
    address: str
    student_class: Optional[Classes] = ""
    class_taught: Optional[Classes] = ""
    reg_date: date


class TeacherBase(BaseModel):
    title: str
    name: str
    email: EmailStr


class TeacherCreate(TeacherBase):
    gender: str
    address: str
    mobile_no: str
    class_taught: Optional[Classes]
    subject_taught: Optional[List[Subject]]
    password: str


class TeacherUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    gender: Optional[str]
    address: Optional[str]
    mobile_no: Optional[str]
    class_taught: Optional[Classes]


class Teacher(TeacherBase):
    id: int
    teacher_id: str
    class_taught: Optional[str]

    class Config:
        orm_mode = True


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
    password: str


class AdminBase(BaseModel):
    name: str
    email: EmailStr


class AdministratorCreate(AdminBase):
    password: str


class AdministratorUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True


class Administrator(AdminBase):
    id: int
    students: list[Students] = []

    class Config:
        orm_mode = True


class GuardianBase(BaseModel):
    title: str
    name: str
    email: EmailStr


class GuardianCreate(GuardianBase):
    password: str
    gender: str
    address: str
    mobile_no: str
    children_id: list[str]


class Guardian(GuardianBase):
    id: int

    class Config:
        orm_mode = True


class Parent(GuardianBase):
    id: int
    children: list[Students]

    class Config:
        orm_mode = True


class LoginBase(BaseModel):
    name: str
    access_token: str
    token_type: str = "bearer"


class AdminLogin(LoginBase):
    email: EmailStr


class StudentLogin(LoginBase):
    id: str


class UserLogin(LoginBase):
    id: str
    role: str


class TokData(BaseModel):
    id: Optional[Any] = None


class NewsBase(BaseModel):
    title: str
    content: str
    category: str


class PostNews(NewsBase):
    pass


class UpdateNews(BaseModel):
    title: Optional[str]
    content: Optional[str]
    category: Optional[str]


class News(PostNews):
    id: int
    date: datetime
    image: Optional[str]
    owner: Admin

    class Config:
        orm_mode = True


class SubjectCreate(BaseModel):
    subjects: list[Subject]
