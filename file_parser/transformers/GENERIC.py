"""
Author: Curtis Larsen <curtis.larsen@utahtech.edu>
Date: 04-05-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import csv
import os
import re
from file_parser.base import BaseTransformer


class GENERIC(BaseTransformer):
    """
    Generic Transformer
    name -> name
    parent_name -> parent_name
    desc -> desc
    """

    __hierarchy__ = "generic"
    __transformer__ = "generic"

    def parse(self):
        """Parse a generic file"""
        if not super().parse():
            return

        #
        # Extract hierarchy name from filename generic_HIERARCHY.csv
        #
        file_name = os.path.basename(self.file_path)
        match = re.match(r"^GENERIC([^A-Za-z0-9])*(.*)\.(csv|CSV)", file_name)
        if match:
            self.__hierarchy__ = match.group(2)

        rows = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                parsed_row = {
                    "name": row.get("name").strip(),
                    "parent_name": row.get("parent_name").strip(),
                    "desc": row.get("desc"),
                }
                rows.append(parsed_row)

        if not rows:
            print("No rows to import")
            return

        self.try_import(rows)
