from datetime import datetime, timedelta
from http import HTTPStatus


def test_make_reservation(client, room, token):
    response = client.post(
        '/reservations',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'start_time': '2025-02-10T04:02:14.296Z',
            'end_time': '2025-02-10T05:02:14.296Z',
            'room_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'start_time': '2025-02-10T04:02:14.296000',
        'end_time': '2025-02-10T05:02:14.296000',
        'room_id': 1,
        'room': {
            'capacity': 10,
            'location': 'Andar 1',
            'name': 'Sala A',
        },
        'user': {
            'user_name': 'João Silva',
        },
    }


def test_start_time_less_than_end_time(client, room, token):
    response = client.post(
        '/reservations',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'start_time': '2025-02-10T05:02:14.296Z',
            'end_time': '2025-02-10T04:02:14.296Z',
            'room_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Start time must be lesser than end time.'}


def test_room_does_not_exist(client, room, token):
    response = client.post(
        '/reservations',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'start_time': str(datetime.now()),
            'end_time': str(datetime.now()),
            'room_id': 2,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Requested room for reservation does not exist.'}


def test_conflicting_reservation(client, room, reservation, token):
    response = client.post(
        '/reservations',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'start_time': str(datetime.now() - timedelta(minutes=30)),
            'end_time': str(datetime.now() + timedelta(minutes=30)),
            'room_id': 1,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'The room is already reserved for this period'}


def test_reservation_same_time_different_rooms(client, room, reservation, token):
    new_room: dict = client.post(
        '/rooms',
        json={
            'name': 'Sala B',
            'capacity': room.capacity,
            'location': room.location,
        },
    ).json()

    start_time = (datetime.now() - timedelta(minutes=30)).isoformat()
    end_time = (datetime.now() + timedelta(minutes=30)).isoformat()

    response = client.post(
        '/reservations',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'start_time': start_time,
            'end_time': end_time,
            'room_id': new_room['id'],
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 2,
        'start_time': start_time,
        'end_time': end_time,
        'room_id': 2,
        'room': {
            'capacity': 10,
            'location': 'Andar 1',
            'name': 'Sala B',
        },
        'user': {
            'user_name': 'João Silva',
        },
    }


def test_cancel_reservation(client, room, reservation, token):
    response = client.delete(
        f'/reservations/{reservation.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_cancel_reservation_without_login(client, room, reservation, token):
    response = client.delete(
        f'/reservations/{reservation.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
