"""
Module: models

This module defines the database models for the application.

Classes:
- Students: Represents the student model in the database.
- Guardians: Represents the guardian model in the database.
- Teacher: Represents the teacher model in the database.
- Admins: Represents the admin model in the database.
- News: Represents the news article model in the database.
- Result: Represents the student result model in the database.
- StudentSubject: Represents the student-subject relationship model in the database.
- TeacherSubject: Represents the teacher-subject relationship model in the database.
- Subjects: Represents the subject model in the database.

Each class corresponds to a table in the database and defines its structure and relationships with other tables.

Note: Before using these models, make sure to establish a connection to the database using SQLAlchemy's `Base` class.
"""

from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, Float


class Students(Base):
    """
    Database model for students.

    Attributes:
        - id (int): Primary key.
        - firstname (str): First name of the student.
        - lastname (str): Last name of the student.
        - middlename (str): Middle name of the student.
        - email (str): Email of the student.
        - address (str): Address of the student.
        - gender (str): Gender of the student.
        - student_class (str): Class of the student.
        - student_id (str): Student ID (unique identifier).
        - password (str): Password of the student.
        - department (str): Department of the student.
        - reg_date (datetime): Registration date of the student.
        - parent_id (int): Foreign key referencing the guardian of the student.
        - teacher_id (int): Foreign key referencing the teacher of the student.

    Relationships:
        - parent (relationship): Relationship with the Guardians model.
        - teacher (relationship): Relationship with the Teacher model.
        - student_subject (relationship): Relationship with the StudentSubject model.
    """

    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    middlename = Column(String)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    student_class = Column(String, nullable=False)
    student_id = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    department = Column(String, nullable=True)
    reg_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    parent_id = Column(Integer, ForeignKey("guardians.id", ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"))

    parent = relationship("Guardians", back_populates="children")
    teacher = relationship("Teacher", back_populates="student")
    student_subject = relationship(
        "StudentSubject", back_populates="student", cascade="all, delete", passive_deletes=True
    )


class Guardians(Base):
    """
    Database model for guardians.

    Attributes:
        - id (int): Primary key.
        - title (str): Title of the guardian.
        - name (str): Name of the guardian.
        - email (str): Email of the guardian (unique identifier).
        - gender (str): Gender of the guardian.
        - address (str): Address of the guardian.
        - mobile_no (str): Mobile number of the guardian.
        - password (str): Password of the guardian.
        - reg_date (datetime): Registration date of the guardian.

    Relationships:
        - children (relationship): Relationship with the Students model.
    """

    __tablename__ = 'guardians'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    children = relationship(
        "Students", back_populates="parent", cascade="all, delete", passive_deletes=True
    )


class Teacher(Base):
    """
    Database model for teachers.

    Attributes:
        - id (int): Primary key.
        - title (str): Title of the teacher.
        - name (str): Name of the teacher.
        - email (str): Email of the teacher (unique identifier).
        - teacher_id (str): Teacher ID (unique identifier).
        - gender (str): Gender of the teacher.
        - address (str): Address of the teacher.
        - mobile_no (str): Mobile number of the teacher.
        - password (str): Password of the teacher.
        - class_taught (str): Class taught by the teacher.
        - reg_date (datetime): Registration date of the teacher.

    Relationships:
        - student (relationship): Relationship with the Students model.
        - teacher_subject (relationship): Relationship with the TeacherSubject model.
    """

    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    teacher_id = Column(String, nullable=False, unique=True)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    mobile_no = Column(String, nullable=False)
    password = Column(String, nullable=False)
    class_taught = Column(String)
    reg_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    student = relationship(
        "Students", back_populates="teacher", cascade="all, delete", passive_deletes=True
    )
    teacher_subject = relationship(
        "TeacherSubject", back_populates="teacher", cascade="all, delete", passive_deletes=True
    )


class Admins(Base):
    """
    Database model for admins.

    Attributes:
        - id (int): Primary key.
        - name (str): Name of the admin.
        - email (str): Email of the admin (unique identifier).
        - password (str): Password of the admin.
        - admin_id (str): Admin ID (unique identifier).
        - reg_date (datetime): Registration date of the admin.

    Relationships:
        - news_article (relationship): Relationship with the News model.
    """

    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin_id = Column(String, nullable=False, unique=True)
    reg_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    news_article = relationship("News", back_populates="owner", cascade="all, delete", passive_deletes=True)


class News(Base):
    """
    Database model for news articles.

    Attributes:
        - id (int): Primary key.
        - title (str): Title of the news article.
        - content (str): Content of the news article.
        - category (str): Category of the news article.
        - image (str): Image associated with the news article.
        - author_id (int): Foreign key referencing the admin author of the news article.
        - date (datetime): Date of the news article.

    Relationships:
        - owner (relationship): Relationship with the Admins model.
    """

    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String)
    author_id = Column(Integer, ForeignKey('admins.id', ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    owner = relationship("Admins", back_populates="news_article")


class Result(Base):
    """
    Database model for student results.

    Attributes:
        - id (int): Primary key.
        - student_subject_id (int): Foreign key referencing the student subject.
        - teacher_subject_id (int): Foreign key referencing the teacher subject.
        - c_a_score (float): Continuous Assessment score.
        - exam_score (float): Exam score.
        - term (str): Term of the result.
        - session (str): Session of the result.
        - time_logged (datetime): Time when the result was logged.

    Relationships:
        - student_subject (relationship): Relationship with the StudentSubject model.
        - teacher_subject (relationship): Relationship with the TeacherSubject model.
    """

    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, nullable=False)
    student_subject_id = Column(Integer, ForeignKey('student_subjects.id', ondelete="CASCADE"), nullable=False)
    teacher_subject_id = Column(Integer, ForeignKey('teacher_subjects.id', ondelete="CASCADE"), nullable=False)
    c_a_score = Column(Float, nullable=False)
    exam_score = Column(Float, nullable=False)
    term = Column(String, nullable=False)
    session = Column(String, nullable=False)
    time_logged = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    student_subject = relationship("StudentSubject", back_populates="result")
    teacher_subject = relationship("TeacherSubject", back_populates="result")


class StudentSubject(Base):
    """
    Database model for student-subject relationship.

    Attributes:
        - id (int): Primary key.
        - student_id (str): Foreign key referencing the student.
        - subject_id (int): Foreign key referencing the subject.

    Relationships:
        - student (relationship): Relationship with the Students model.
        - subject (relationship): Relationship with the Subjects model.
        - result (relationship): Relationship with the Result model.
    """

    __tablename__ = 'student_subjects'
    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(String, ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"), nullable=False)

    student = relationship("Students", back_populates="student_subject")
    subject = relationship("Subjects", back_populates="student_subject")
    result = relationship(
        "Result", back_populates="student_subject", cascade="all, delete", passive_deletes=True
    )


class TeacherSubject(Base):
    """
    Database model for teacher-subject relationship.

    Attributes:
        - id (int): Primary key.
        - teacher_id (int): Foreign key referencing the teacher.
        - subject_id (int): Foreign key referencing the subject.

    Relationships:
        - teacher (relationship): Relationship with the Teacher model.
        - subject (relationship): Relationship with the Subjects model.
        - result (relationship): Relationship with the Result model.
    """

    __tablename__ = 'teacher_subjects'
    id = Column(Integer, primary_key=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"), nullable=False)

    teacher = relationship("Teacher", back_populates="teacher_subject")
    subject = relationship("Subjects", back_populates="teacher_subject")
    result = relationship(
        "Result", back_populates="teacher_subject", cascade="all, delete", passive_deletes=True
    )


class Subjects(Base):
    """
    Database model for subjects.

    Attributes:
        - id (int): Primary key.
        - subject (str): Name of the subject (unique identifier).

    Relationships:
        - student_subject (relationship): Relationship with the StudentSubject model.
        - teacher_subject (relationship): Relationship with the TeacherSubject model.
    """

    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, nullable=False)
    subject = Column(String, nullable=False, unique=True)

    student_subject = relationship(
        "StudentSubject", back_populates="subject", cascade="all, delete", passive_deletes=True
    )
    teacher_subject = relationship(
        "TeacherSubject", back_populates="subject", cascade="all, delete", passive_deletes=True
    )
