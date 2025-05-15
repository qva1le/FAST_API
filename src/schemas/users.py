from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str



class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

class User(UserAdd):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)