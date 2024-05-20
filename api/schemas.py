"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 04-05-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class HierarchyType(Enum):
    """Classification hierarchy types"""

    UN_SPSC_CODES = "UN_SPSC"
    US_PTC_CODES = "US_PTC"
    US_ECCN_PARTS = "US_ECCN"
    EU_ECCN_PARTS = "EU_ECCN"
    TAXON_A = "TAXON_A"
    TAXON_B = "TAXON_B"
    TAXON_C = "TAXON_C"
    TAXON_D = "TAXON_D"
    TAXON_E = "TAXON_E"
    TAXON_F = "TAXON_F"
    TAXON_G = "TAXON_G"
    TAXON_H = "TAXON_H"
    TAXON_I = "TAXON_I"
    TAXON_J = "TAXON_J"
    TAXON_K = "TAXON_K"
    TAXON_L = "TAXON_L"


class Item(BaseModel):
    """Item model."""

    name: str
    description: str
    categories: list[str]
    hierarchy: HierarchyType


class Classification(BaseModel):
    """Classification model."""

    name: str
    description: str
    confidence: float
    hierarchy: Optional[HierarchyType] = Field(
        None, description="Classification hierarchy type"
    )


class Config(BaseModel):
    """Configuration model for classify endpoint."""

    hierarchy: Optional[HierarchyType] = Field(
        None, description="Classification hierarchy type"
    )


class ClassifyInputConfig(Config):
    """Configuration model for classify endpoint."""

    variant: str


class ClassifyInput(BaseModel):
    """Input model for classify endpoint."""

    name: str
    description: str
    categories: list[str]
    config: ClassifyInputConfig


class ClassifyOutput(BaseModel):
    """Output model for classify endpoint."""

    data: list[Classification]
    response_time_ms: float


class ClassificationTreeNode(BaseModel):
    """Classification tree node model."""

    name: str
    description: str
    confidence: float
    accepted: bool
    children: list["ClassificationTreeNode"] = []


class ClassificationTreeInput(BaseModel):
    """Input model for classifications_tree endpoint."""

    classification_id: int


class ClassificationTreeOutput(BaseModel):
    """Output model for classifications_tree endpoint."""

    roots: list[ClassificationTreeNode]
