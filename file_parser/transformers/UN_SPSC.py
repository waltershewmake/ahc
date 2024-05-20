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


class UN_SPSC(BaseTransformer):
    """
    UN Standard Product and Services Transformer

    Segment,Family,Class,Commodity -> name
    Family,Class,Commodity -> parent_name
    Segment Name, Family Name, Class Name, Commodity Name -> desc

    UNSPSC is an 8 digit hierarchical code. Every two digits of the code is a different level of the hierarchy.
    For instance consider 50415534, this code is for Organic serrano peppers, it's parent 50415500 identifies Organic peppers.
    50415500's parent 50410000 identifies Organic fresh vegetables, and finally it's parent 50000000 identifies Food Beverage
    and Tobacco Products. In this transformer we store each level as it's own node. For instance 14111616 and it's parent 14110000
    would both be stored. Each item stores it's name, description and parent (except for segment items like 50000000 since they
    have no parent, for them we just store an empty list)
    """

    __hierarchy__ = "UN_SPSC"
    __transformer__ = "UN_SPSC"

    def parse(self):
        """Parse US product tax codes file"""
        if not super().parse():
            return

        rows = []
        code_tracker = set()
        with open(
            self.file_path, "r", encoding="utf-8", errors="replace"
        ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                _segment = row.get("Segment").strip()
                _family = row.get("Family").strip()
                _class = row.get("Class").strip()
                _commodity = row.get("Commodity").strip()
                if _segment in code_tracker:
                    pass
                else:
                    code_tracker.add(_segment)
                    parsed_row = {
                        "name": _segment,
                        "parent_name": "",
                        "desc": row.get("Segment Name").strip(),
                    }
                    rows.append(parsed_row)

                if _family in code_tracker:
                    pass
                else:
                    code_tracker.add(_family)
                    parsed_row = {
                        "name": _family,
                        "parent_name": _segment,
                        "desc": row.get("Family Name").strip(),
                    }
                    rows.append(parsed_row)

                if _class in code_tracker:
                    pass
                else:
                    code_tracker.add(_class)
                    parsed_row = {
                        "name": _class,
                        "parent_name": _family,
                        "desc": row.get("Class Name").strip(),
                    }
                    rows.append(parsed_row)

                if _commodity in code_tracker:
                    pass
                else:
                    code_tracker.add(_commodity)
                    parsed_row = {
                        "name": _commodity,
                        "parent_name": _class,
                        "desc": row.get("Commodity Name").strip(),
                    }
                    rows.append(parsed_row)
        if not rows:
            print("No rows to import")
            return

        self.try_import(rows)
