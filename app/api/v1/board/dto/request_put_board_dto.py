from pydantic import BaseModel, Field


class RequestPutBoardDTO(BaseModel):
    title: str = Field(..., max_length=100)
    contents: str
