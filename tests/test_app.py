from http import HTTPStatus


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
    assert response.json() == {
        'rooms': [
            {
                'name': 'Sala A',
                'capacity': 10,
                'location': 'Andar 1',
                'id': 1,
            }
        ]
    }
