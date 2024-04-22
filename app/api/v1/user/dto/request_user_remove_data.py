from pydantic import BaseModel


class RequestUserRemoveDataDTO(BaseModel):
    email: str
