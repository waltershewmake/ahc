"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from pgvector.sqlalchemy import Vector

from db.base import Base


class HSCodeVector(Base):
    """HS Code model with vectorized representation."""

    __tablename__ = "hs_code_vector"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("file.id"), nullable=False)
    hierarchy_id = Column(Integer, ForeignKey("hierarchy.id"), nullable=False)

    file = relationship("File")
    hierarchy = relationship("Hierarchy")
    embedding = mapped_column(Vector(3072))

    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, index=True)
