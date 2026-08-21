"""
Main module for the Widget Platform API.
"""
from fastapi import FastAPI

app = FastAPI(
    title="Embeddable Widget & Lead-Capture Platform",
    description="Backend API for managing widgets and capturing leads."
)


@app.get("/")
def read_root():
    """
    Root endpoint to verify the server is running.
    """
    return {"message": "Widget Platform API is running!"}