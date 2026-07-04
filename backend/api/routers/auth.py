from fastapi import APIRouter, Depends, Request
from infrastructure.mysql.user_db import get_session
from sqlalchemy.orm import Session

from api.schemas.auth_info import AuthInfo
from api.services import auth_service

router = APIRouter()


@router.post("/auth")
def auth(
    *, request: Request, db: Session = Depends(get_session), auth_info: AuthInfo
):
    user_id = auth_service.authenticate(db, auth_info)
    request.session["user_id"] = user_id
    return {"message": "Authenticated"}
