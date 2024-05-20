"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from db.models import Hierarchy, HSCode


def get_by_hierarchy(
    db,
    hierarchy,
) -> list[HSCode]:
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
) -> HSCode:
    """Get HS code by name."""

    hs_code = db.query(HSCode).filter(HSCode.name == name).first()
    return hs_code


def get_by_desc(
    db,
    desc: str,
) -> HSCode:
    """Get HS code by description."""

    hs_code = db.query(HSCode).filter(HSCode.description == desc).first()
    return hs_code


def get_hierarchy_roots(
    db,
    hierarchy,
) -> list[HSCode]:
    """Get HS codes by hierarchy, where parent_id is NULL."""

    hierarchy = (
        db.query(Hierarchy).filter(Hierarchy.name == hierarchy.value).first()
    )

    if hierarchy is None:
        raise ValueError(f"Hierarchy '{hierarchy.value}' not found.")

    # get all hs_codes for hierarchy where parent_id is NULL
    hs_codes = (
        db.query(HSCode)
        .filter(HSCode.hierarchy_id == hierarchy.id, HSCode.parent_id.is_(None))
        .all()
    )

    return hs_codes


def get_path_to_root(
    db,
    hs_code: HSCode,
) -> list[HSCode]:
    """Get the path to the root of the hierarchy."""

    path = [hs_code]

    while hs_code.parent_id is not None:
        hs_code = (
            db.query(HSCode).filter(HSCode.id == hs_code.parent_id).first()
        )
        path.append(hs_code)

    return path[::-1]
