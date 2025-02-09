from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from reserva.database import get_session
from reserva.models import Room
from reserva.schemas import (
    FilterPage,
    RoomDB,
    RoomList,
    RoomSchema,
)

router = APIRouter(prefix='/rooms', tags=['rooms'])

Session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK, response_model=RoomList)
def list_rooms(session: Session, filter_rooms: Annotated[FilterPage, Query()]):
    rooms = session.scalars(
        select(Room)
        .offset(filter_rooms.offset * filter_rooms.limit)
        .limit(filter_rooms.limit)
    ).all()
    return {'rooms': rooms}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=RoomDB)
def create_room(room: RoomSchema, session: Session):
    db_room = session.scalar(select(Room).where(Room.name == room.name))
    if db_room:
        if db_room.name == room.name:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Room '{room.name}' already exists.",
            )

    db_room = Room(
        name=room.name, capacity=room.capacity, location=room.location
    )

    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room
