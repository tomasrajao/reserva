from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Room:
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capacity: Mapped[int]
    location: Mapped[str]
    reservations: Mapped[list['Reservation']] = relationship(
        init=False, back_populates='room', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    user_name: Mapped[str]
    password: Mapped[str]
    reservations: Mapped[list['Reservation']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class Reservation:
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(init=False, back_populates='reservations')

    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    room: Mapped[Room] = relationship(init=False, back_populates='reservations')
