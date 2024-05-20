"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import os

from classifier.pipelines.openai_embeddings import bulk_vectorize
from db.models import File, Hierarchy, HSCode, HSCodeVector
from db.services.hs_code_service import get_path_to_root


class BaseTransformer:
    """Base transformer class to expose an extensible interface for parsing and importing files into the database."""

    __hierarchy__ = None
    __transformer__ = None

    def __init__(self, db, file_path):
        self.db = db
        self.file_path = file_path

    def parse(self):
        """Parse a file"""

        if not self._should_parse():
            return False

        print(
            f"Parsing file {self.file_path} with transformer {self.__transformer__}"
        )
        return True

    def _should_parse(self):
        """Check if the file should be parsed"""

        if not self.__hierarchy__:
            print("No hierarchy specified for transformer")
            return False

        if not self.__transformer__:
            print("No transformer specified for transformer")
            return False

        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} does not exist")
            return False

        file = self.db.query(File).filter_by(path=self.file_path).first()

        if file:
            print(f"File {self.file_path} has already been imported. Skipping.")
            return False

        return True

    def _should_import(self):
        """Ensure the hierarchy exists in the database before importing the file"""

        hierarchy = (
            self.db.query(Hierarchy).filter_by(name=self.__hierarchy__).first()
        )

        if not hierarchy:
            try:
                self.db.add(Hierarchy(name=self.__hierarchy__))
                self.db.commit()
            except Exception as e:
                print(f"Error adding hierarchy {self.__hierarchy__}: {e}")
                return False

        return True

    def try_import(self, data):
        """Try to import a file into the database"""

        print(f"Attempting to insert rows for {self.__hierarchy__}")

        if not self._should_import():
            print(f"Skipping import for {self.file_path}")
            return

        # Get the hierarchy
        hierarchy = (
            self.db.query(Hierarchy).filter_by(name=self.__hierarchy__).first()
        )

        # Insert the file into the database
        file = File(
            hierarchy_id=hierarchy.id,
            name=os.path.basename(self.file_path),
            path=self.file_path,
            size=os.path.getsize(self.file_path),
        )

        self.db.add(file)
        self.db.flush()

        nodes = {row["name"]: row for row in data}

        # Insert the nodes into the database without parent-child relationships
        for node in nodes.values():
            self.db.add(
                HSCode(
                    file_id=file.id,
                    hierarchy_id=hierarchy.id,
                    name=node["name"],
                    description=node["desc"],
                )
            )

        self.db.flush()

        # add the parent-child relationships
        for node in nodes.values():
            if node["parent_name"] in nodes:
                parent = nodes[node["parent_name"]]
                child = nodes[node["name"]]

                parent_node = (
                    self.db.query(HSCode).filter_by(name=parent["name"]).first()
                )

                if not parent_node:
                    print(
                        f"Parent node {parent['name']} not found for child node {child['name']}"
                    )
                    continue

                self.db.query(HSCode).filter_by(name=child["name"]).update(
                    {"parent_id": parent_node.id}
                )

        self.db.flush()

        items_to_vectorize = []
        hs_codes = self.db.query(HSCode).filter_by(file_id=file.id).all()
        hs_codes_without_children = [
            hs_code for hs_code in hs_codes if not hs_code.children
        ]

        # we only want to vectorize the leaf nodes
        for hs_code in hs_codes_without_children:
            path_to_root = get_path_to_root(self.db, hs_code)

            description = " -> ".join(
                [node.description for node in path_to_root]
            )

            items_to_vectorize.append(
                (
                    hs_code,
                    description,
                )
            )

        embeddings = bulk_vectorize([item[1] for item in items_to_vectorize])

        for i, (hs_code, _) in enumerate(items_to_vectorize):
            self.db.add(
                HSCodeVector(
                    file_id=file.id,
                    hierarchy_id=hierarchy.id,
                    name=hs_code.name,
                    description=items_to_vectorize[i][1],
                    embedding=embeddings[i],
                )
            )

        self.db.commit()

        print(f"File {self.file_path} has been imported")
