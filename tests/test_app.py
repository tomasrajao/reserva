from http import HTTPStatus

from reserva.schemas import RoomDB, UserPublic


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


def test_list_rooms(client):
    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': []}


def test_list_rooms_with_rooms(client, room):
    room_schema = RoomDB.model_validate(room).model_dump()

    response = client.get('/rooms/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'rooms': [room_schema]}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'user_name': 'João Silva',
            'email': 'joao_silva@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'user_name': 'João Silva',
        'email': 'joao_silva@email.com',
        'id': 1,
    }


def test_list_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'user_name': 'João Silva ',
            'email': 'joao_silva@email.com',
            'password': 'outro_secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_name': 'João Silva ',
        'email': 'joao_silva@email.com',
        'id': 1,
    }


def test_update_integrity_error(client, user):
    response = client.post(
        '/users/',
        json={
            'user_name': 'José Souza ',
            'email': 'jose_souza@email.com',
            'password': '123321',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'user_name': 'João Silva ',
            'email': 'jose_souza@email.com',
            'password': 'outro_secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists.'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}
