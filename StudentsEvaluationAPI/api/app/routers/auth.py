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
