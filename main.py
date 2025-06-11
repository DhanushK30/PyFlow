from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "API is up!",
        "environment": os.getenv("ENV", "dev")
    }
