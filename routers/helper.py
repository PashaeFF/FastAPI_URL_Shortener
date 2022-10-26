import requests
from fastapi.security import HTTPBasicCredentials,HTTPBearer
from fastapi import Depends

url = "" #your token check url :)

def token_cheker(token):
    response_verify = requests.get(url, headers = {'Authorization': 'Bearer '+ token })
    if response_verify.ok:
        return True
    else:
        return False

def has_token(credentials: HTTPBasicCredentials = Depends(HTTPBearer())):
    return credentials.credentials
