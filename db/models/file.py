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


class File(Base):
    """File model."""

    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    hierarchy_id = Column(Integer, ForeignKey("hierarchy.id"), nullable=False)

    hierarchy = relationship("Hierarchy")

    name = Column(String, index=True, unique=True, nullable=False)
    path = Column(String, index=True, unique=True, nullable=False)
    size = Column(Integer, index=True, nullable=False)
