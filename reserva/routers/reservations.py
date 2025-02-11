from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from reserva.app import logger
from reserva.database import get_session
from reserva.models import Reservation, Room, User
from reserva.schemas import ReservationPublic, ReservationSchema
from reserva.security import get_current_user

router = APIRouter(prefix='/reservations', tags=['reservations'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ReservationPublic)
def reserve_room(reservation: ReservationSchema, session: Session, current_user: CurrentUser):
    if reservation.start_time >= reservation.end_time:
        logger.error('BAD REQUEST: start_time greater than end_time.')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Start time must be lesser than end time.')

    room = session.scalar(select(Room).where(Room.id == reservation.room_id))

    if not room:
        logger.error('BAD REQUEST: Room does not exist.')
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Requested room for reservation does not exist.')

    query = select(Reservation).where(Reservation.room_id == room.id)
    query = query.filter(
        or_(
            and_(
                reservation.start_time <= Reservation.start_time,
                Reservation.start_time >= reservation.end_time,
            ),
            and_(
                reservation.start_time <= Reservation.end_time,
                Reservation.end_time >= reservation.end_time,
            ),
        )
    )
    if session.scalars(query).all():
        logger.error('CONFLICT: reservation period conflicting.')
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='The room is already reserved for this period.',
        )

    db_reservation = Reservation(
        start_time=reservation.start_time,
        end_time=reservation.end_time,
        room_id=reservation.room_id,
        user_id=current_user.id,
    )

    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)

    logger.info(f'CREATED: Reservation for {db_reservation.room.name} created successfuly.')
    return db_reservation


@router.delete('/{reservation_id}', status_code=HTTPStatus.NO_CONTENT)
def cancel_reservation(reservation_id: int, session: Session, current_user: CurrentUser):
    reservation = session.scalar(select(Reservation).where(Reservation.id == reservation_id))

    if not reservation:
        logger.error('NOT FOUND: Reservation does not exist.')
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Reservation not found.',
        )

    if current_user.id != reservation.user_id:
        logger.error('FORBIDDEN: User has no permission to cancel this reservation.')
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions.',
        )

    session.delete(reservation)
    session.commit()
    logger.info('OK: Reservation canceled.')
