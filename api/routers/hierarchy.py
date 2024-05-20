"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from fastapi import APIRouter

from api.dependencies import Session
from db.models import Hierarchy
from db.models.hs_code import HSCode
from db.services.hierarchy_service import get_one


router = APIRouter()


@router.get("/hierarchies")
async def get_hierarchies(db: Session):
    """Get all hierarchies."""

    hierarchies = db.query(Hierarchy).all()

    # add the number of HS Codes in each hierarchy
    return [
        {
            **hierarchy.__dict__,
            "hs_code_count": db.query(HSCode)
            .filter(HSCode.hierarchy_id == hierarchy.id)
            .count(),
        }
        for hierarchy in hierarchies
    ]


@router.get("/hierarchy/{hierarchy_name}")
async def get_hierarchy(db: Session, hierarchy_name: str):
    """Get a specific hierarchy of HS Codes."""

    hierarchy = get_one(db, hierarchy_name)

    if hierarchy is None:
        return {"error": "Hierarchy not found"}

    return {
        **hierarchy.__dict__,
        "hs_codes": db.query(HSCode)
        .filter(HSCode.hierarchy_id == hierarchy.id)
        .all(),
    }
