from pydantic import BaseModel, ConfigDict, EmailStr


class RoomSchema(BaseModel):
    name: str
    capacity: int
    location: str
    model_config = ConfigDict(from_attributes=True)


class RoomDB(RoomSchema):
    id: int


class RoomList(BaseModel):
    rooms: list[RoomDB]


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


class Message(BaseModel):
    message: str
