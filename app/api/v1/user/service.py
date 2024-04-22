import bcrypt

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from starlette import status

from app.api.dependency import auth_handler
from app.api.v1.user.dto.request_user_profile_dto import RequestUserProfileDTO
from app.api.v1.user.dto.request_user_remove_data import RequestUserRemoveDataDTO
from app.api.v1.user.dto.request_user_sign import RequestUserSignUpDTO
from app.api.v1.user.dto.request_user_sign_dto import RequestUserSigninDTO

from app.api.v1.user.entity.user import User
from app.api.v1.user.utils import PasswordBcrypt
from app.config.redis_config import redis_session


def post_user_signup(db_session: Session, data: RequestUserSignUpDTO):
    if (
        is_email_check := db_session.execute(
            select(User).filter(User.email == data.email)
        ).scalar_one_or_none()
    ) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already"
        )

    data.password = PasswordBcrypt.generate_password_hash(data.password)

    db_session.execute(
        insert(User).values(
            name=data.name,
            email=data.email,
            password=data.password,
        )
    )
    db_session.commit()

    return None


def post_user_signin(
    db_session: Session,
    data: RequestUserSigninDTO,
):
    if (
        user_data := db_session.execute(
            select(User).filter(User.email == data.email)
        ).scalar_one_or_none()
    ) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email does not exist"
        )

    is_verified = PasswordBcrypt.check_password_hash(data.password, user_data.password)

    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect"
        )
    access_token = auth_handler.encode_token(user_data.email, "access")
    redis_session.set(
        f"user_refresh_token:{access_token}",
        auth_handler.encode_token(user_data.email, "refresh"),
        60 * 60 * 2,
    )
    return {"access_token": access_token}


def put_user_profile(user, db_session: Session, data: RequestUserProfileDTO):
    user_data = db_session.execute(
        select(User).filter(User.email == user["email"])
    ).scalar_one_or_none()
    if data.check_password is not None:
        is_verified_password = PasswordBcrypt.check_password_hash(
            data.check_password, user_data.password
        )
        if not is_verified_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Password is incorrect"
            )
    if data.password is not None:
        data.password = PasswordBcrypt.generate_password_hash(data.password)
        user_data.password = data.password
    if data.name is not None:
        user_data.name = data.name

    db_session.add(user_data)
    db_session.commit()

    return True


def put_user_sign_remove(user, db_session: Session, data: RequestUserRemoveDataDTO):
    user_data = db_session.execute(
        select(User).filter(User.email == data.email)
    ).scalar_one_or_none()

    user_data.is_session = 1

    db_session.add(user_data)
    db_session.commit()

    return True
