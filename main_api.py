from fastapi import FastAPI
from app.routes.event_routes import router as event_router

app = FastAPI(
    title="Calendar Assistant API",
    description="API for managing calendar events with AI assistance.",
    version="1.0.0"
)

app.include_router(event_router, prefix="/events", tags=["events"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
