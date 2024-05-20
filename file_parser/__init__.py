"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 04-12-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import os

from .transformers.EU_ECCN import EU_ECCN
from .transformers.US_ECCN import US_ECCN
from .transformers.US_PTC import US_PTC
from .transformers.UN_SPSC import UN_SPSC
from .transformers.GENERIC import GENERIC

__all__ = ["EU_ECCN", "US_ECCN", "US_PTC", "UN_SPSC"]


def try_parse(db, file_path):
    """Try to parse a file using its prefix to determine the transformer to use"""

    # open file and get file name
    with open(file_path, "r", encoding="utf-8") as file:
        # get file name (without the path)
        file_name = os.path.basename(file.name)

    # check if any transformer name prefixes the file name
    transformer = None
    for prefix in __all__:
        if file_name.startswith(prefix):
            transformer = globals()[f"{prefix}"](db, file_path)
            break
    if not transformer:
        # if no transformer found, try to use the generic transformer
        transformer = GENERIC(db, file_path)

    # parse the file
    if transformer:
        transformer.parse()
    else:
        print(f"No transformer found for file {file_path}")
