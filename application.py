"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-19-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from fastapi import FastAPI
from api.routers import hierarchy_router, classify_router


def create_app():
    """Create the FastAPI app."""

    _app = FastAPI()

    _app.include_router(hierarchy_router)
    _app.include_router(classify_router)

    return _app


app = create_app()


@app.get("/ping")
def index() -> str:
    """Health check endpoint."""

    return "pong!"
