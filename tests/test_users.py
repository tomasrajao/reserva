from http import HTTPStatus

from reserva.schemas import UserPublic


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


def test_create_existing_user(client, user):
    UserPublic.model_validate(user).model_dump()

    response = client.post(
        '/users/',
        json={
            'user_name': 'João Silva ',
            'email': 'joao_silva@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': "User 'joao_silva@email.com' already exists."
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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_update_user_integrity_error(client, user, token):
    response = client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_name': 'José Souza ',
            'email': 'jose_souza@email.com',
            'password': '123321',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_name': 'João Silva ',
            'email': 'jose_souza@email.com',
            'password': 'outro_secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists.'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}
