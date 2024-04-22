from typing import Optional

from pydantic import BaseModel


class RequestUserProfileDTO(BaseModel):
    check_password: Optional[str]
    password: Optional[str]
    name: Optional[str]
