"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from contextlib import contextmanager

from .base import Base
from .session import Session
from .engine import engine

from . import models


try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
except Exception as e:
    print(f"Error occurred: {e}")


def get_db():
    """Get a database connection."""

    _db = Session()
    try:
        yield _db
    finally:
        _db.close()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""

    _db = Session()
    try:
        yield _db
        _db.commit()
    except:
        _db.rollback()
        raise
    finally:
        _db.close()
