from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
    name: str
    capacity: int
    location: str
    model_config = ConfigDict(from_attributes=True)


class RoomDB(RoomSchema):
    id: int


class RoomList(BaseModel):
    rooms: list[RoomDB]
