from typing import Union
from pydantic import BaseModel, BaseSettings, HttpUrl

class ShortUrl(BaseModel):
    url_title: str
    url: str

class Settings(BaseSettings):
    ...

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class Auth(BaseModel):
    token: str
