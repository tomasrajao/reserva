from http import HTTPStatus

from fastapi import FastAPI

from reserva.schemas import RoomDB, RoomList, RoomSchema

app = FastAPI()
database = []


@app.get('/rooms/', status_code=HTTPStatus.OK, response_model=RoomList)
def list_rooms():
    return {'rooms': database}


@app.post('/rooms/', status_code=HTTPStatus.CREATED, response_model=RoomDB)
def create_room(room: RoomSchema):
    room_id = len(database) + 1
    room_with_id = RoomDB(**room.model_dump(), id=room_id)
    database.append(room_with_id)
    return room_with_id
