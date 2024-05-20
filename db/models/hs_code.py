"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class HSCode(Base):
    """HS Code model with parent-child relationship."""

    __tablename__ = "hs_code"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("file.id"), nullable=False)
    hierarchy_id = Column(Integer, ForeignKey("hierarchy.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("hs_code.id"), nullable=True)

    file = relationship("File")
    hierarchy = relationship("Hierarchy")
    parent = relationship("HSCode", remote_side=[id], backref="children")

    name = Column(
        String, index=True, unique=True, nullable=False
    )  # Should be unique because it forms the parent-child relationship
    description = Column(String, index=True)
