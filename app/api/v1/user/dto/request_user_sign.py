import re
from pydantic import BaseModel, field_validator


class RequestUserSignUpDTO(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        is_valid_password = bool(
            re.match(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                v,
            )
        )

        if not is_valid_password:
            raise ValueError("Invalid password")
        return v
