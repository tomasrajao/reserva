from fastapi import FastAPI

from reserva.routers import auth, reservations, rooms, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(reservations.router)
app.include_router(rooms.router)
app.include_router(users.router)
