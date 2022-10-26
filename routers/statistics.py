from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import models, database, paginate
from routers import url_visits



stat = APIRouter(
    tags=['Statistics'],
    prefix= ("/statistics")
)     

@stat.get('/')
async def get_stats(db: Session =  Depends(database.get_db), page_num: int = 1, page_size: int = 1):
    data = []
    data_length = len(data)
    all_urls = db.query(models.UrlShortener).order_by(
        models.UrlShortener.visits_count.desc())
    
    for item in all_urls:
        view_stats = {
            'id': item.id,
            'Site URL': item.url,
            'Visits count': item.visits_count,
            'Date Created': item.created_at
        }
        data.append(view_stats)

    return paginate.paginate(data, data_length, page_num,page_size)

@stat.get('/{id}')
async def get_stats_id(id, db: Session = Depends(database.get_db)):
    data = []
    items = db.query(models.UrlVisitors).filter_by(url_id = id).order_by(models.UrlVisitors.device_visits_count.desc()).all()

    for item in items:
        view_stats = {
            'id': item.id,
            'User ID': item.user_id,
            'Device IP': item.device_ip,
            'Device visits count': item.device_visits_count,
            'Date Created': item.device_visit_date
        }

        data.append(view_stats)

    return {'data': data}, status.HTTP_200_OK