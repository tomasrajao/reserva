from http import HTTPStatus


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={
            'Authorization': 'Bearer token-ivalido',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials.'}
