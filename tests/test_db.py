from dataclasses import asdict

from sqlalchemy import select

from reserva.models import Room


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
    }
