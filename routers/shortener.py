from urllib import response
from fastapi import APIRouter, Depends, status, HTTPException, Header, status
from sqlalchemy.orm import Session
import models, database, schemas
from routers.auth import get_check_token
from .helper import token_cheker, has_token

short = APIRouter(
    tags=['Urls'],
    prefix='/shorts'
)

@short.post("/", status_code=status.HTTP_201_CREATED, tags=["Url Shortener"])
async def handle_short_url(request: schemas.ShortUrl, db: Session = Depends(database.get_db), token= Depends(has_token)):
    if token:
        new_url = models.UrlShortener(url_title = request.url_title, url = request.url)
        test_url = db.query(models.UrlShortener).filter_by(url = request.url).first()
        if test_url:
            return {'detail':'URL is available'}
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return new_url
    else:
        return {"message": "Unauthorized"}


@short.get("/{id}", status_code=status.HTTP_200_OK)
async def get_short_url(id: int, db: Session = Depends(database.get_db), token= Depends(has_token)):
    if token:
        created_url = db.query(models.UrlShortener).filter_by(id=id).first()
        if not created_url:
            return {'detail': f'{id} not found'}, status.HTTP_404_NOT_FOUND
        return created_url
    else:
        return {"message": "Unauthorized"}

@short.get("/", status_code=status.HTTP_200_OK)
async def short_urls(db: Session = Depends(database.get_db), token= Depends(has_token)):
    if token:
        urls = db.query(models.UrlShortener).all()
        return urls
    else:
        return {"message": "Unauthorized"}

@short.delete("/{id}", status_code=status.HTTP_200_OK)
async def destroy_url(id: int, db: Session = Depends(database.get_db), token= Depends(has_token)):
    if token:
        created_url = db.query(models.UrlShortener).filter_by(id=id).first()
        if not created_url:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"URL with the id {id} is not available")
        db.delete(created_url)
        db.commit()
        return {'detail': f'{id} deleted'}
    else:
        return {"message": "Unauthorized"}

@short.put("/{id}", status_code=status.HTTP_200_OK)
async def update_url(id: int, request: schemas.ShortUrl, db: Session = Depends(database.get_db), token= Depends(has_token)):
    if token:
        created_url = db.query(models.UrlShortener).filter_by(id=id)
        if not created_url.first():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"URL with the id {id} is not available")
        created_url.update({'url_title': request.url_title, 'url': request.url }, synchronize_session= False)
        db.commit()
        return {'detail': f'{id} updated'}
    else:
        return {"message": "Unauthorized"}