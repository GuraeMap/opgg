import math
from typing import Optional, Literal

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette import status

from app.api.v1.board.dto.request_delete_board_dto import RequestDeleteBoardDto
from app.api.v1.board.dto.request_post_board_dto import RequestPostBoardDTO
from app.api.v1.board.dto.request_put_board_dto import RequestPutBoardDTO
from app.api.v1.board.entity.board import Board
from app.api.v1.user.entity.user import User


def get_board(
    current_page: int,
    field: Optional[Literal["view_count", "created_at"]],
    db_session: Session,
):
    """
    한 페이지당 게시글 10개씩 볼 수 있음.
    """
    total_page = (
        db_session.execute(select(Board).order_by(-Board.id).limit(1)).scalars().first()
    )

    if total_page is not None:
        total_page = math.ceil(total_page.id / 10)
    else:
        total_page = 1

    sql = select(Board)
    match field:
        case None:
            ...
        case "view_count":
            sql = sql.order_by(-Board.view_count)
        case "created_at":
            sql = sql.order_by(-Board.created_at)

    sql = sql.offset((current_page - 1) * 10).limit(10)

    data = db_session.execute(sql)
    data = data.scalars().all()
    return {"total_page": total_page, "board_data": data}


def post_board(user, db_session: Session, data: RequestPostBoardDTO):
    user_data = db_session.execute(
        select(User).filter(User.email == user["email"])
    ).scalar_one_or_none()
    db_session.execute(
        insert(Board).values(
            title=data.title, contents=data.contents, user_id=user_data.id
        )
    )
    db_session.commit()

    return True


def get_board_id(db_session: Session, board_id: int):
    board_data = db_session.get(Board, board_id)
    if board_data.updated_at is None:
        board_updated_at = ""
    else:
        board_updated_at = board_data.updated_at

    board_data.view_count += 1
    res_data = dict(
        usr_name=(
            board_data.user.name if not board_data.user.is_session else "탈퇴한 유저"
        ),
        title=board_data.title,
        contents=board_data.contents,
        created_at=board_data.created_at,
        updated_at=board_updated_at,
    )

    #
    db_session.add(board_data)
    db_session.commit()

    return res_data


def put_board_id(
    user,
    db_session: Session,
    data: RequestPutBoardDTO,
    board_id: int,
):
    board_data = db_session.get(Board, board_id)
    user_data = db_session.execute(
        select(User).filter(User.email == user["email"])
    ).scalar_one_or_none()

    if board_data.user_id != user_data.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Board User Not Matching"
        )

    board_data.title = data.title
    board_data.contents = data.contents
    db_session.add(board_data)
    db_session.commit()

    return True


def delete_board(user, db_session: Session, data: RequestDeleteBoardDto):
    board_data = db_session.get(Board, data.id)
    user_data = db_session.execute(
        select(User).filter(User.email == user["email"])
    ).scalar_one_or_none()

    if board_data.user_id != user_data.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Board User Not Matching"
        )

    db_session.delete(board_data)
    db_session.commit()

    return True
