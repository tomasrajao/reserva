from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from reserva.database import get_session
from reserva.models import Room, User
from reserva.schemas import Message, RoomDB, RoomList, RoomSchema, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/rooms/', status_code=HTTPStatus.OK, response_model=RoomList)
def list_rooms(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    rooms = session.scalars(select(Room).offset(skip * limit).limit(limit)).all()
    return {'rooms': rooms}


@app.post('/rooms/', status_code=HTTPStatus.CREATED, response_model=RoomDB)
def create_room(room: RoomSchema, session: Session = Depends(get_session)):
    db_room = session.scalar(select(Room).where(Room.name == room.name))
    if db_room:
        if db_room.name == room.name:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Room '{room.name}' already exists.")

    db_room = Room(name=room.name, capacity=room.capacity, location=room.location)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def list_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip * limit).limit(limit)).all()
    return {'users': users}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"User '{user.email}' already exists.")
    db_user = User(user_name=user.user_name, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found.')

    try:
        db_user.user_name = user.user_name
        db_user.password = user.password
        db_user.email = user.email

        session.commit()
        session.refresh(db_user)
    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists.')

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found.')

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted.'}
