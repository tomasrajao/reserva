from pydantic import BaseModel

# , ConfigDict, FutureDatetime


class RoomSchema(BaseModel):
    name: str
    capacity: int
    location: str


class RoomDB(RoomSchema):
    id: int


class RoomList(BaseModel):
    rooms: list[RoomDB]
