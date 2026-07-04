from api.schemas.auth_info import AuthInfo

from fastapi import APIRouter

router = APIRouter()


@router.post("/auth")
def auth(auth_info: AuthInfo):
    print(auth_info.email)
    return {"message": "Authenticated"}
