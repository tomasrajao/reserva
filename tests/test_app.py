from http import HTTPStatus

from reserva.schemas import RoomDB


def test_create_room(client):
    room = {
        'name': 'Sala A',
        'capacity': 10,
        'location': 'Andar 1',
    }
    response = client.post('/rooms/', json=room)

    room['id'] = response.json()['id']

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == room


def test_list_rooms(client):
    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': []}


def test_list_rooms_with_rooms(client, room):
    room_schema = RoomDB.model_validate(room).model_dump()

    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': [room_schema]}
