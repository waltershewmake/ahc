"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from pgvector.sqlalchemy import Vector
from sqlalchemy import label, select

from db.models import Hierarchy, HSCodeVector


def get_by_hierarchy(
    db,
    hierarchy,
) -> list[HSCodeVector]:
    """Get HS codes by hierarchy."""

    hierarchy = (
        db.query(Hierarchy).filter(Hierarchy.name == hierarchy.value).first()
    )

    if hierarchy is None:
        raise ValueError(f"Hierarchy '{hierarchy.value}' not found.")

    return hierarchy.hs_codes


def get_by_name(
    db,
    name: str,
) -> HSCodeVector:
    """Get HS code by name."""

    hs_code = db.query(HSCodeVector).filter(HSCodeVector.name == name).first()
    return hs_code


def get_by_desc(
    db,
    desc: str,
) -> HSCodeVector:
    """Get HS code by description."""

    hs_code = (
        db.query(HSCodeVector).filter(HSCodeVector.description == desc).first()
    )
    return hs_code


def get_nearest_neighbors(
    db,
    vector: Vector,
    hierarchy: Hierarchy = None,
    n: int = 3,
):
    """
    Retrieves vectors similar to a given vector, optionally filtering by hierarchy.
    Orders by cosine distance to give a distance score and includes this score in the results.
    TODO: ^^ this doesn't accurately reflect model confidence. How do we determine confidence?
    """

    if hierarchy:
        hierarchy_instance = (
            db.query(Hierarchy)
            .filter(Hierarchy.name == hierarchy.value)
            .first()
        )
        if not hierarchy_instance:
            return []

        query = (
            select(
                label(
                    "distance", HSCodeVector.embedding.cosine_distance(vector)
                ),
                HSCodeVector,
            )
            .where(HSCodeVector.hierarchy_id == hierarchy_instance.id)
            .order_by(HSCodeVector.embedding.cosine_distance(vector))
            .limit(n)
        )
    else:
        query = (
            select(
                label(
                    "distance", HSCodeVector.embedding.cosine_distance(vector)
                ),
                HSCodeVector,
            )
            .order_by(HSCodeVector.embedding.cosine_distance(vector))
            .limit(n)
        )

    results = db.execute(query).fetchall()
    return [(1 - result[0], result[1]) for result in results]


def get_similarity(
    vector1: HSCodeVector,
    vector2: HSCodeVector,
):
    """
    Retrieves the cosine similarity between two vectors.
    """

    return 1 - vector1.embedding.cosine_distance(vector2.embedding)
