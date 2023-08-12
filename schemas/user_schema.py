import datetime

from typing import Optional, List

from pydantic import BaseModel, EmailStr

from schemas.parking_schema import ParkingSchema


class UserSchemaBase(BaseModel):
    user_id: Optional[str] = None
    name: str
    email: EmailStr
    is_Admin: bool = False
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaParkings(UserSchemaBase):
    parkings: Optional[List[ParkingSchema]]


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_Admin: Optional[bool] = None
