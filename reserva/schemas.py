from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr

Date = date


class RoomSchema(BaseModel):
    name: str
    capacity: int
    location: str
    model_config = ConfigDict(from_attributes=True)


class RoomPublic(RoomSchema):
    id: int


class RoomList(BaseModel):
    rooms: list[RoomPublic]


class Username(BaseModel):
    user_name: str


class UserPublic(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class ReservationSchema(BaseModel):
    start_time: datetime
    end_time: datetime
    room_id: int
    model_config = ConfigDict(from_attributes=True)


class ReservationPublic(ReservationSchema):
    id: int
    room: RoomSchema
    user: Username


class ReservationList(BaseModel):
    reservations: list[ReservationPublic]


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class FilterPeriod(BaseModel):
    start_time: datetime
    end_time: datetime


class FilterDate(BaseModel):
    date: Date | None = None
    offset: int = 0
    limit: int = 100
