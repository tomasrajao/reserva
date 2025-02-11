import sys

from fastapi import FastAPI
from loguru import logger

from reserva.routers import auth, reservations, rooms, users

logger.remove()
logger.add(sink='logfile.log')
logger.add(sink=sys.stderr)

app = FastAPI()

app.include_router(auth.router)
app.include_router(reservations.router)
app.include_router(rooms.router)
app.include_router(users.router)
