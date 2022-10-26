
from fastapi import APIRouter, status
from .helper import token_cheker

check = APIRouter(
    tags=['Check'],
    prefix= ("/check")
)     


@check.get('/')
def get_check_token(token):
    return token_cheker(token)
