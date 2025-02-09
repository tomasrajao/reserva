from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from reserva.database import get_session
from reserva.models import Room
from reserva.schemas import RoomDB, RoomList, RoomSchema

app = FastAPI()
database = []


@app.get('/rooms/', status_code=HTTPStatus.OK, response_model=RoomList)
def list_rooms(skip: int = 0, limit: int = 1, session: Session = Depends(get_session)):
    rooms = session.scalars(select(Room).offset(skip * limit).limit(limit)).all()
    return {'rooms': rooms}


@app.post('/rooms/', status_code=HTTPStatus.CREATED, response_model=RoomDB)
def create_room(room: RoomSchema, session: Session = Depends(get_session)):
    db_room = session.scalar(select(Room).where(Room.name == room.name))
    if db_room:
        if db_room.name == room.name:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Room '{room.name}' already exists.")

    db_room = Room(name=room.name, capacity=room.capacity, location=room.location)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room
