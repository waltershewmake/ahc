"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Hierarchy(Base):
    """Hierarchy model."""

    __tablename__ = "hierarchy"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True, nullable=False)

    hs_codes = relationship("HSCode", back_populates="hierarchy")
