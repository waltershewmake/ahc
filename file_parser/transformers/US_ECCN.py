"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 04-12-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import csv
from file_parser.base import BaseTransformer


class US_ECCN(BaseTransformer):
    """
    US ECCN Transformer

    part_id -> name
    parent_id -> parent_name
    eccn_desc -> desc
    """

    __hierarchy__ = "US_ECCN"
    __transformer__ = "US_ECCN"

    def parse(self):
        """Parse a us_eccn file"""
        if not super().parse():
            return

        rows = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                parsed_row = {
                    "name": row.get("part_id").strip(),
                    "parent_name": row.get("parent_id").strip(),
                    "desc": row.get("eccn_desc"),
                }
                rows.append(parsed_row)

        if not rows:
            print("No rows to import")
            return

        self.try_import(rows)
