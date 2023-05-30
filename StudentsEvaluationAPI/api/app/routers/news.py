from typing import Optional
from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2
from cloudinary.uploader import upload


router = APIRouter(tags=["News letter"], prefix="/newsletter")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.News)
async def create_news(
        news: schemas.PostNews, db: Session = Depends(database.get_db),
        admin: models.Admins = Depends(oauth2.get_admin_user),
        file: Optional[UploadFile] = None
):
    """
    Create a new news article.

    This endpoint allows an admin user to create a new news article.
    The article can include an optional image file, which will be uploaded to Cloudinary.

    Parameters:
    - news: The news article data.
    - db: Database session dependency.
    - admin: Currently authenticated admin user.
    - file: Optional image file associated with the news article.

    Returns:
    The newly created news article.
    """
    new_news = models.News(author_id=admin.id, **news.dict())
    if file:
        # delete the file from memory and rollover to disk to save unnecessary memory space
        file.file.rollover()
        file.file.flush()

        valid_types = [
            'image/png',
            'image/jpeg',
            'image/bmp',
        ]
        await utils.validate_file(file, 11000000, valid_types)
        pics = upload(file.file)
        url = pics.get("url")
        new_news.image = url

    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news


@router.delete("/{newsID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(
        newsID: int, db: Session = Depends(database.get_db),
        admin: int = Depends(oauth2.get_admin_user)
):
    """
    Delete a news article.

    This endpoint allows an admin user to delete a news article by its ID.

    Parameters:
    - newsID: The ID of the news article to delete.
    - db: Database session dependency.
    - admin: Currently authenticated admin user.

    Returns:
    None.
    """
    return


@router.get("/{newsID}", response_model=schemas.News)
async def get_news(
        newsID: int, db: Session = Depends(database.get_db),
):
    """
    Get a news article by its ID.

    This endpoint retrieves a news article by its ID.

    Parameters:
    - newsID: The ID of the news article to retrieve.
    - db: Database session dependency.

    Returns:
    The requested news article.
    """
    news = db.query(models.News).filter(models.News.id == newsID).all()
    return news


async def update_news(
        newsID: int, news: schemas.UpdateNews, db: Session = Depends(database.get_db),
        _: models.News = Depends(oauth2.get_admin_user),
        file: Optional[UploadFile] = None
):
    """
    Update a news article.

    This endpoint allows an admin user to update a news article by its ID.
    The article can include an optional image file, which will be uploaded to Cloudinary.

    Parameters:
    - newsID: The ID of the news article to update.
    - news: The updated news article data.
    - db: Database session dependency.
    - admin: Currently authenticated admin user.
    - file: Optional image file associated with the news article.

    Returns:
    The updated news article.
    """
    found_news = db.query(models.News).where(models.News.id == newsID).first()
    if file:
        # delete the file from memory and rollover to disk to save unnecessary memory space
        file.file.rollover()
        file.file.flush()

        valid_types = [
            'image/png',
            'image/jpeg',
            'image/bmp',
        ]
        await utils.validate_file(file, 11000000, valid_types)
        pics = upload(file.file)
        url = pics.get("url")
        found_news.image = url

    found_news.update(news)
    db.commit()
    db.refresh(found_news)
    return found_news
