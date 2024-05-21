"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 04-12-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import time
from fastapi import APIRouter, HTTPException

from api.dependencies import Session
from api.schemas import ClassifyInput, ClassifyOutput
import classifier.variants as variants


router = APIRouter(
    tags=["classify"],
    responses={404: {"description": "Not found"}},
)


@router.post("/classify")
async def classify(body: ClassifyInput, db: Session):
    """Generate a classification calculation and return the result."""

    item = {
        "name": body.name,
        "description": body.description,
        "categories": body.categories,
    }

    config = body.config

    variant = config.variant

    if variant not in variants.__all__:
        raise HTTPException(
            status_code=404,
            detail=f"Variant '{variant}' not found.",
        )

    classify_fn = getattr(variants, variant)

    start_time = time.time()

    classifications = await classify_fn(db, item, config)

    end_time = time.time()

    return ClassifyOutput(
        data=classifications,
        response_time_ms=(end_time - start_time) * 1000,
    )
