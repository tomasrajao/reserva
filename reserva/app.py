from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from reserva.database import get_session
from reserva.models import Room, User
from reserva.schemas import (
    Message,
    RoomDB,
    RoomList,
    RoomSchema,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from reserva.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()


@app.get('/rooms/', status_code=HTTPStatus.OK, response_model=RoomList)
def list_rooms(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    rooms = session.scalars(
        select(Room).offset(skip * limit).limit(limit)
    ).all()
    return {'rooms': rooms}


@app.post('/rooms/', status_code=HTTPStatus.CREATED, response_model=RoomDB)
def create_room(room: RoomSchema, session: Session = Depends(get_session)):
    db_room = session.scalar(select(Room).where(Room.name == room.name))
    if db_room:
        if db_room.name == room.name:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Room '{room.name}' already exists.",
            )

    db_room = Room(
        name=room.name, capacity=room.capacity, location=room.location
    )

    session.add(db_room)
    session.commit()
    session.refresh(db_room)

    return db_room


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def list_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(
        select(User).offset(skip * limit).limit(limit)
    ).all()
    return {'users': users}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"User '{user.email}' already exists.",
            )
    db_user = User(
        user_name=user.user_name,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )
    try:
        current_user.user_name = user.user_name
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        session.commit()
        session.refresh(current_user)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists.'
        )

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions.'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted.'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password.',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password.',
        )

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
