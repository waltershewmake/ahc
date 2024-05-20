"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 04-05-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import argparse
import os

from db import session_scope
from . import try_parse


if __name__ == "__main__":
    # get the file path from the command line
    parser = argparse.ArgumentParser(description="Parse a file")
    parser.add_argument("file", help="The file to parse")

    args = parser.parse_args()

    # try to parse the file
    with session_scope() as db:
        try_parse(db, os.path.abspath(args.file))
