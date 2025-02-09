from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Room:
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    capacity: Mapped[int]
    location: Mapped[str]


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    user_name: Mapped[str]
    password: Mapped[str]
