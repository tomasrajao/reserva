from http import HTTPStatus

from reserva.schemas import RoomDB


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
    RoomDB.model_validate(room).model_dump()

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
    room_schema = RoomDB.model_validate(room).model_dump()

    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': [room_schema]}
