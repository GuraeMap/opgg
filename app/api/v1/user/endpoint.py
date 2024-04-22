from fastapi import APIRouter

from app.api.v1.user import service
from app.api.v1.user.dto.request_user_profile_dto import RequestUserProfileDTO
from app.api.v1.user.dto.request_user_remove_data import RequestUserRemoveDataDTO
from app.api.v1.user.dto.request_user_sign import RequestUserSignUpDTO
from app.api.v1.user.dto.request_user_sign_dto import RequestUserSigninDTO
from app.config.db.database import DbSession
from app.api.dependency import user

api = APIRouter(prefix="/user", tags=["user"])


@api.post(
    "/sign-up",
    response_description="""
    <H1> 회원 가입 Post </H1>
    """,
)
def post_user_signup(db_session: DbSession, data: RequestUserSignUpDTO):
    return service.post_user_signup(db_session, data)


@api.post(
    "/sign-in",
    response_description="""
    <H1> 로그인 Post </H1>
    """,
)
def post_user_signin(db_session: DbSession, data: RequestUserSigninDTO):
    return service.post_user_signin(db_session, data)


@api.put(
    "/profile",
    response_description="""
    <H1> 유저 프로필 수정 Post </H1>
    """,
)
def put_user_profile(user: user, db_session: DbSession, data: RequestUserProfileDTO):
    return service.put_user_profile(user, db_session, data)


@api.put(
    "/sign-remove",
    response_description="""
    <H1> 회원 탈퇴 </H1>
    """,
)
def put_sign_remove(user: user, db_session: DbSession, data: RequestUserRemoveDataDTO):
    return service.put_user_sign_remove(user, db_session, data)
