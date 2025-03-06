from pydantic import BaseModel, EmailStr


class SUsers(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class SUsersRequestAdd(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class SUsersRequestAuth(BaseModel):
    email: EmailStr
    password: str


class SUsersAdd(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str


class SUsersWithHashedPassword(SUsers):
    hashed_password: str
