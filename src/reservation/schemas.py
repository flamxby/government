from pydantic import BaseModel, validator
from datetime import date, datetime
from typing import List, Optional


class ReservationBase(BaseModel):
    register_timestamp: datetime


class Reservation(ReservationBase):
    class Config:
        orm_mode = True


class ReservationForUser(BaseModel):
    reservation_id: int
    register_timestamp: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    surname: str
    citizen_id: str
    birth_date: date
    occupation: str
    address: str
    password: str

    @validator("citizen_id")
    def check_citizen_id(cls, value: str):
        if not value.isdigit():
            raise ValueError("citizen id must be a digit")
        if len(value) != 13:
            raise ValueError("citizen id must have 13 digits")
        return value


class ShowUser(BaseModel):
    user_id: int
    name: str
    surname: str
    citizen_id: str
    occupation: str
    address: str
    reservations: List[ReservationForUser] = []

    class Config:
        orm_mode = True


class ShowUserInfo(BaseModel):
    name: str
    surname: str
    birth_date: date
    citizen_id: str
    occupation: str
    address: str

    class Config:
        orm_mode = True


class ShowReservation(BaseModel):
    reservation_id: int
    register_timestamp: datetime
    vaccinated: bool
    owner: ShowUserInfo

    class Config:
        orm_mode = True


class Login(BaseModel):
    citizen_id: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    citizen_id: Optional[str] = None


class UnauthorizedResponse(BaseModel):
    detail: Optional[str] = "Not authenticated"


class NotFoundResponse(BaseModel):
    detail: Optional[str] = "No reservation with this id"


class NoPermissionResponse(BaseModel):
    detail: Optional[str] = "No permission"
