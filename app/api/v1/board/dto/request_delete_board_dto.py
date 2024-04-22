from pydantic import BaseModel


class RequestDeleteBoardDto(BaseModel):
    id: int
