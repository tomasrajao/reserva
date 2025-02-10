from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from reserva.database import get_session
from reserva.models import Reservation, Room
from reserva.schemas import (
    FilterDate,
    FilterPage,
    FilterPeriod,
    Message,
    ReservationList,
    RoomList,
    RoomPublic,
    RoomSchema,
)

router = APIRouter(prefix='/rooms', tags=['rooms'])

Session = Annotated[Session, Depends(get_session)]


@router.get('/', status_code=HTTPStatus.OK, response_model=RoomList)
def list_rooms(session: Session, filter_rooms: Annotated[FilterPage, Query()]):
    rooms = session.scalars(
        select(Room).offset(filter_rooms.offset * filter_rooms.limit).limit(filter_rooms.limit)
    ).all()
    return {'rooms': rooms}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=RoomPublic)
def create_room(room: RoomSchema, session: Session):
    db_room = session.scalar(select(Room).where(Room.name == room.name))
    if db_room:
        if db_room.name == room.name:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Room '{room.name}' already exists.",
            )

    db_room = Room(name=room.name, capacity=room.capacity, location=room.location)

    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room


@router.get('/{room_id}/availability', status_code=HTTPStatus.OK, response_model=Message)
def get_room_availability(room_id: int, session: Session, filter_rooms: Annotated[FilterPeriod, Query()]):
    if not (filter_rooms.start_time and filter_rooms.end_time):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Must inform both start_time and end_time')

    room = session.scalar(select(Room).where(Room.id == room_id))

    if not room:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Room does not exist.')

    query = select(Reservation).where(Reservation.room_id == room.id)

    query = query.filter(
        or_(
            and_(
                Reservation.start_time < filter_rooms.start_time,
                filter_rooms.start_time < Reservation.end_time,
            ),
            and_(
                Reservation.start_time < filter_rooms.end_time,
                filter_rooms.end_time < Reservation.end_time,
            ),
        )
    )
    if session.scalars(query).all():
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='The room is already reserved for this period',
        )

    return {'message': f'{room.name} is available from {filter_rooms.start_time} to {filter_rooms.end_time}'}


@router.get('/{room_id}/reservations', status_code=HTTPStatus.OK, response_model=ReservationList)
def get_room_reservations(room_id: int, session: Session, filter_reservations: Annotated[FilterDate, Query()]):
    room = session.scalar(select(Room).where(Room.id == room_id))

    if not room:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Room does not exist.')

    query = select(Reservation).where(Reservation.room_id == room.id)

    if filter_reservations.date:
        query = query.filter(func.date(Reservation.start_time) == filter_reservations.date)

    query = query.offset(filter_reservations.offset).limit(filter_reservations.limit)
    reservations = session.scalars(query).all()

    if not reservations:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No room reservations for this date.',
        )

    return {'reservations': reservations}
