from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models, database, schemas
import requests
from starlette.responses import HTMLResponse, RedirectResponse



visit_url = APIRouter(
    tags=['Redirect to url']
)

@visit_url.get('/{short_url}')
async def redirect_to_url(short_url: str, db: Session =  Depends(database.get_db)):
    link = db.query(models.UrlShortener).filter_by(short_url=short_url).first()
    if link:
        r = requests.get('http://google.com')
        agent = r.request.headers.get('User-Agent') #user agent
        where = "" #It shows which link the user came from
        ip_address = '12.12.1.26' #user IP
        user = "af83b713-d2a1-4f1e-bc37-2ddd270d2db4" #user UUID
        r.status_code

        updated = db.query(models.UrlVisitors).filter_by(url_id=link.id, where = "link", browser_info = agent, device_ip = ip_address, user_id = user).first()

        if not updated:
            visitor = models.UrlVisitors(url_id=link.id, where = where, browser_info = agent, device_ip=ip_address, user_id = user)
            link.visits_count += 1
            print("link: ", link)
        
            db.add(visitor)
            db.commit()
            db.refresh(visitor)

        else:
            updated.device_visits_count += 1
            db.add(updated)
            db.commit()
            db.refresh(updated)
        response = RedirectResponse(url=link.url)
        return response
    else:
        return {'error':'Not Found'}
        