"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from sqlalchemy.orm import sessionmaker

from .engine import engine


Session = sessionmaker(bind=engine)
