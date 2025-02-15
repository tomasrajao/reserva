from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from reserva.app import app
from reserva.database import get_session
from reserva.models import Reservation, Room, User, table_registry
from reserva.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def room(session):
    room = Room(name='Sala A', capacity=10, location='Andar 1')

    session.add(room)
    session.commit()
    session.refresh(room)

    return room


@pytest.fixture
def user(session):
    password = 'secret'
    user = User(
        user_name='João Silva',
        email='joao_silva@email.com',
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def reservation(session, user):
    reservation = Reservation(
        room_id=1,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
        user_id=user.id,
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation
