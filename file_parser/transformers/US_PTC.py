"""
Author: Colby Starr
Date: 04-05-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import csv
from file_parser.base import BaseTransformer


class US_PTC(BaseTransformer):
    """
    US Product Tax Codes Transformer

    matrix_sku -> name
    parent_sku -> parent_name
    description -> desc
    """

    __hierarchy__ = "US_PTC"
    __transformer__ = "US_PTC"

    def parse(self):
        """Parse US product tax codes file"""
        if not super().parse():
            return

        rows = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                parsed_row = {
                    "name": row.get("matrix_sku").strip(),
                    "parent_name": row.get("parent_sku").strip(),
                    "desc": row.get("description"),
                }
                rows.append(parsed_row)
        if not rows:
            print("No rows to import")
            return

        self.try_import(rows)
