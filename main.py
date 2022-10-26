from fastapi import FastAPI
from routers import auth, shortener, url_visits, statistics
import models, database
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.include_router(auth.check)
app.include_router(shortener.short)
app.include_router(url_visits.visit_url)
app.include_router(statistics.stat)
