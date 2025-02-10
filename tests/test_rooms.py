from datetime import date, datetime, timedelta
from http import HTTPStatus

from reserva.schemas import RoomPublic


def test_create_room(client):
    response = client.post(
        '/rooms/',
        json={
            'name': 'Sala A',
            'capacity': 10,
            'location': 'Andar 1',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'Sala A',
        'capacity': 10,
        'location': 'Andar 1',
        'id': 1,
    }


def test_create_existing_room(client, room):
    RoomPublic.model_validate(room).model_dump()

    response = client.post(
        '/rooms/',
        json={
            'name': 'Sala A',
            'capacity': 10,
            'location': 'Andar 1',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': "Room 'Sala A' already exists.",
    }


def test_list_rooms(client):
    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': []}


def test_list_rooms_with_rooms(client, room):
    room_schema = RoomPublic.model_validate(room).model_dump()

    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': [room_schema]}


def test_room_is_available(client, room, reservation):
    params = {
        'start_time': datetime.now() + timedelta(hours=4),
        'end_time': datetime.now() + timedelta(hours=6),
    }
    response = client.get(f'/rooms/{room.id}/availability', params=params)
    assert response.json() == {
        'message': f'{room.name} is available from {params["start_time"]} to {params["end_time"]}'
    }


def test_room_is_not_available():
    pass


def test_room_with_reservations(client, room, reservation):
    start_time = reservation.start_time.isoformat()
    end_time = reservation.end_time.isoformat()

    response = client.get(f'/rooms/{room.id}/reservations', params={'date': date.today()})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'reservations': [
            {
                'end_time': end_time,
                'id': 1,
                'room': {
                    'capacity': 10,
                    'location': 'Andar 1',
                    'name': 'Sala A',
                },
                'room_id': 1,
                'start_time': start_time,
                'user': {
                    'user_name': 'João Silva',
                },
            }
        ],
    }


def test_no_reservations_on_informed_date(client, room, reservation):
    response = client.get(f'/rooms/{room.id}/reservations', params={'date': date.today() + timedelta(days=1)})

    assert response.json() == {'detail': 'No room reservations for this date.'}


def test_one_reservation_on_informed_date(client, room, reservation, token):
    start_time = (datetime.now() + timedelta(days=1)).isoformat()
    end_time = (datetime.now() + timedelta(days=1, hours=1)).isoformat()

    new_reservation = client.post(
        '/reservations',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'room_id': 1,
            'start_time': start_time,
            'end_time': end_time,
        },
    )

    response = client.get(f'/rooms/{room.id}/reservations', params={'date': date.today() + timedelta(days=1)})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'reservations': [new_reservation.json()]}
