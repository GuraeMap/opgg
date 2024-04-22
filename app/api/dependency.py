from datetime import datetime, timedelta

import jwt
from typing import Literal, Annotated

from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

from app.config.config import defalut
from app.config.redis_config import redis_session


class AuthHandler:
    def __call__(self, req: Request):
        token = req.headers.get("Authorization", None)

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authorization header is required",
            )

        _, token = token.split("Bearer ")

        payload = self.decode_token(token)

        return payload

    def encode_token(self, email, type: Literal["access", "refresh"]):

        if type == "access":
            token_exp = datetime.utcnow() + timedelta(hours=1)

        else:
            token_exp = datetime.utcnow() + timedelta(days=1)

        payload = {
            "exp": token_exp,
            "iat": datetime.utcnow(),
            "token_type": type,
            "email": email,
        }
        return jwt.encode(payload, defalut.JWT_SECRET_KEY, algorithm="HS256")

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, defalut.JWT_SECRET_KEY, algorithms="HS256")

        except jwt.ExpiredSignatureError:
            refresh_token = redis_session.get(f"user_refresh_token:{token}")
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Expired token"
                )
            payload = jwt.decode(
                refresh_token, defalut.JWT_SECRET_KEY, algorithms="HS256"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )
        return payload


auth_handler = AuthHandler()


##
user = Annotated[dict, Depends(auth_handler)]
