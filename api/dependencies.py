"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from typing import Annotated
from fastapi import Depends

from db import session_scope, get_db


Session = Annotated[session_scope, Depends(get_db)]
