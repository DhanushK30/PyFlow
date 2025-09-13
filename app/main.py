# app/main.py
from contextlib import asynccontextmanager  
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import workflows  # Import the workflows router

# This is an event handler that runs when the FastAPI application starts.
# We use it to create our database and tables.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(
    title="PyFlow API",
    description="An API-first automation engine inspired by Zapier.",
    version="1.0.0",
    lifespan=lifespan # Add the lifespan event handler
)

# Include the router from the workflows.py file.
# This makes the endpoints defined in that router available in our app.
app.include_router(workflows.router)


@app.get("/", tags=["Health Check"])
def read_root():
    """
    This is the root endpoint of the API.
    It's a simple health check to confirm the server is running.
    """
    return {"status": "ok", "message": "Welcome to PyFlow API!"}