from fastapi import APIRouter
from app.api.v1.user.endpoint import api as user_api
from app.api.v1.board.endpoint import api as board_api


api = APIRouter(prefix="/v1")


api.include_router(user_api)
api.include_router(board_api)
