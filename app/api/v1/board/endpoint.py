from typing import Optional, Literal, Annotated

from fastapi import APIRouter, Query, Path

from app.api.v1.board import service
from app.api.v1.board.dto.request_delete_board_dto import RequestDeleteBoardDto
from app.api.v1.board.dto.request_post_board_dto import RequestPostBoardDTO
from app.api.v1.board.dto.request_put_board_dto import RequestPutBoardDTO

from app.api.v1.board.entity.board import Board
from app.config.db.database import DbSession

from app.api.dependency import user


api = APIRouter(prefix="/board", tags=["board"])


@api.get(
    "/",
)
def get_board(
    db_session: DbSession,
    current_page: Optional[int] = Query(1, description="현재 페이지 "),
    field: Optional[Literal["view_count", "created_at"]] = Query(
        None, description="조회 방법"
    ),
):
    return service.get_board(
        current_page,
        field,
        db_session,
    )


@api.post(
    "/",
    response_description="""
    <H1> 게시글 작성 Post </H1>
    """,
)
def post_board(
    user: user,
    db_session: DbSession,
    data: RequestPostBoardDTO,
):
    return service.post_board(user, db_session, data)


@api.get("/{board_id}")
def get_board_id(
    db_session: DbSession, board_id: int = Path(..., description="게시글 ID")
):
    return service.get_board_id(db_session, board_id)


@api.put(
    "/{board_id}",
)
def put_board_id(
    user: user,
    db_session: DbSession,
    data: RequestPutBoardDTO,
    board_id: int = Path(..., description="게시글 ID"),
):
    return service.put_board_id(user, db_session, data, board_id)


@api.delete("/")
def delete_board(
    user: user,
    db_session: DbSession,
    data: RequestDeleteBoardDto,
):
    return service.delete_board(user, db_session, data)
