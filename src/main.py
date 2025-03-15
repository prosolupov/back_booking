import uvicorn
from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as room_router
from src.api.bookings import router as booking_router
from src.api.facilities import router as facility_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(booking_router)
app.include_router(facility_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
