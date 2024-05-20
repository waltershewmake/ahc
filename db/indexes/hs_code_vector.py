"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from sqlalchemy import Index

from db.models.hs_code_vector import HSCodeVector


hs_code_vector_index = Index(
    "hs_code_vector_embedding_idx",
    HSCodeVector.embedding,
    postgresql_using="ivfflat",
    postgres_with={"lists": 100},
    postgres_ops={"factors": "vector_cosine_ops"},
)
