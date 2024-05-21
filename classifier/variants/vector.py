"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 04-15-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from api.dependencies import Session
from api.schemas import Classification, Config, Item
from classifier.pipelines.openai_embeddings import vectorize_async
from db.services.hs_code_vector_service import get_nearest_neighbors


def item_to_text(item):
    """
    Convert an item object into a text string to classify.
    There is room to try various formatting options here to see what
    kinds of language features help the classifier.
    """

    s = "item is named {:s}.".format(item["name"])
    for category in item["categories"]:
        s += " {:s} belongs to the category {:s}.".format(
            item["name"], category
        )

    if item["description"] is not None:
        s += " {:s} is described by {:s}.".format(
            item["name"], item["description"]
        )
    return s


async def classify(
    db: Session,
    item: Item,
    config: Config,
):
    """Vectorize an item and find the N most similar items"""

    vector = await vectorize_async(item_to_text(item))

    top_n = get_nearest_neighbors(
        db=db, hierarchy=config.hierarchy, vector=vector, n=5
    )

    return [
        Classification(
            name=item.name,
            description=item.description,
            hierarchy=item.hierarchy.name,
            confidence=confidence,
        )
        for confidence, item in top_n
    ]
