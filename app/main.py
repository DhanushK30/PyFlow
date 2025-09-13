# app/main.py

from fastapi import FastAPI

# Create an instance of the FastAPI class
# The title and version will be displayed in the API docs (Swagger UI)
app = FastAPI(
    title="PyFlow API",
    description="An API-first automation engine inspired by Zapier.",
    version="1.0.0"
)

# Define your first API endpoint
# @app.get("/") is a "decorator" that tells FastAPI that the function below
# is responsible for handling GET requests to the root URL ("/").
@app.get("/", tags=["Health Check"])
def read_root():
    """
    This is the root endpoint of the API.
    It's a simple health check to confirm the server is running.
    """
    return {"status": "ok", "message": "Welcome to PyFlow API!"}