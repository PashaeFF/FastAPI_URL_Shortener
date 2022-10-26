from enum import unique
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from database import Base
from datetime import datetime
import random, string
from fastapi import Depends
from database import get_db

class UrlShortener(Base):
    __tablename__ = 'url_shortner'

    id = Column(Integer, primary_key=True)
    url_title = Column(Text, nullable=True)
    url = Column(Text, nullable=False, unique =True)
    short_url = Column(String, nullable=True)
    visits_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())
    visitors = relationship("UrlVisitors", backref="urls")

    def generate_short_characters(self):
        
        characters = string.digits + string.ascii_letters
        pciked_chars = ''.join(random.choices(characters,k=4))
        db = get_db()
        link = db.query(UrlShortener).filter_by(short_url=pciked_chars).first()
        while not link:
            return pciked_chars
  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return self.short_url

class UrlVisitors(Base):
    __tablename__ = "url_visitors" 

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable = True)
    url_id = Column(Integer, ForeignKey("url_shortner.id"))
    where = Column(String, nullable=False)
    browser_info = Column(String(120), unique=False, nullable=False)
    device_ip = Column(String(120), nullable=False)
    device_visits_count = Column(Integer, default=1)
    device_visit_date = Column(DateTime, default=datetime.now())
