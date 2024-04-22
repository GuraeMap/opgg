from pydantic import BaseModel, Field


class RequestPostBoardDTO(BaseModel):
    title: str = Field(..., max_length=100)
    contents: str
