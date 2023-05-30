from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2

router = APIRouter(tags=["Guardians"], prefix="/guardian")


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.Guardian)
async def create_guardian(
    user: schemas.GuardianCreate, db: Session = Depends(database.get_db),
    _: str = Depends(oauth2.get_admin_user)
):
    """
    Create Guardian

    Creates a new guardian in the system and associates them with their children.

    Parameters:
    - user (schemas.GuardianCreate): Data of the guardian to be created.
    - db (Session): SQLAlchemy Session object for database operations.
    - role (str): Role of the authenticated user. (Depends on OAuth2 token)

    Returns:
    - schemas.Guardian: Created guardian with assigned ID.

    Raises:
    - HTTPException(403): If the user does not have sufficient privileges.

    """
    hashed_pwd = utils.hashed(user.password)
    user.password = hashed_pwd
    children = user.children_id
    del user.children_id
    new_user = models.Guardians(**user.dict())
    db.add(new_user)

    for _id in children:
        db.query(models.Students).filter(
            models.Students.student_id == _id
        ).update({"parent_id": new_user.id}, synchronize_session=False)
        db.commit()

    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete("/{userID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guardian(
    userID: int, db: Session = Depends(database.get_db),
    _: str = Depends(oauth2.get_admin_user)
):
    """
    Delete Guardian

    Deletes a guardian from the system.

    Parameters:
    - userID (int): ID of the guardian to be deleted.
    - db (Session): SQLAlchemy Session object for database operations.
    - role (str): Role of the authenticated user. (Depends on OAuth2 token)

    Returns:
    - None

    Raises:
    - HTTPException(403): If the user does not have sufficient privileges.

    """
    db.query(models.Guardians).where(models.Guardians.id == userID).delete()
    db.commit()
    return


@router.put("/password", status_code=status.HTTP_200_OK)
async def change_password(
    form_data: schemas.UpdatePassword,
    user: models.Guardians = Depends(oauth2.get_guardian),
    db: Session = Depends(database.get_db)
):
    """
    Change Password

    Changes the password of a guardian.

    Parameters:
    - form_data (schemas.UpdatePassword): Data containing old and new passwords.
    - user (models.Guardians): Authenticated guardian.
    - db (Session): SQLAlchemy Session object for database operations.

    Returns:
    - dict: Dictionary with a success message.

    Raises:
    - HTTPException(404): If the old password is incorrect.
    - HTTPException(409): If the new password and confirmation password do not match.

    """
    if not utils.verify(form_data.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    if form_data.new_password != form_data.password:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Passwords do not match")
    user.update({"password": utils.hashed(form_data.new_password)}, synchronize_session=False)
    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully"}


@router.get("/", response_model=list[schemas.Guardian])
async def get_all_parents(
    db: Session = Depends(database.get_db),
    _: models.Admins = Depends(oauth2.get_admin_user)
):
    """
    Get All Parents

    Retrieves a list of all guardians in the system.

    Parameters:
    - db (Session): SQLAlchemy Session object for database operations.
    - user (models.Admins): Authenticated admin user.

    Returns:
    - List[schemas.Guardian]: List of all guardians.

    Raises:
    - HTTPException(403): If the user does not have sufficient privileges.

    """
    return db.query(models.Guardians).all()
