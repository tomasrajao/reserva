from dataclasses import asdict
from datetime import datetime, timedelta

from sqlalchemy import select

from reserva.models import Reservation, Room, User


def test_create_room(session):
    new_room = Room(name='Sala A', capacity=10, location='Andar 1')

    session.add(new_room)
    session.commit()

    room = session.scalar(select(Room).where(Room.name == 'Sala A'))

    assert asdict(room) == {
        'id': 1,
        'name': 'Sala A',
        'capacity': 10,
        'location': 'Andar 1',
        'reservations': [],
    }


def test_create_user(session):
    new_user = User(user_name='João Silva', email='joao_silva@gmail.com', password='secret')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.user_name == 'João Silva'))

    assert asdict(user) == {
        'id': 1,
        'user_name': 'João Silva',
        'email': 'joao_silva@gmail.com',
        'password': 'secret',
        'reservations': [],
    }


def test_create_reservation(session, user: User, room: Room):
    reservation = Reservation(
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
        user_id=user.id,
        room_id=room.id,
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    room = session.scalar(select(Room).where(Room.id == room.id))

    user = session.scalar(select(User).where(User.id == user.id))

    assert reservation in room.reservations
    assert reservation in user.reservations
