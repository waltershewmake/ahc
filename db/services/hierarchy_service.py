"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from api.dependencies import Session
from db.models.hierarchy import Hierarchy


def get_one(db: Session, hierarchy_name: str):
    """Get a specific hierarchy of HS Codes."""

    hierarchy = (
        db.query(Hierarchy).filter(Hierarchy.name == hierarchy_name).first()
    )

    return hierarchy
