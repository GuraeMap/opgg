from pydantic import BaseModel


class RequestUserSigninDTO(BaseModel):
    email: str
    password: str
