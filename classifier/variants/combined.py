"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 07-11-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from api.dependencies import Session
from api.schemas import Classification, Config, Item

from classifier.pipelines.openai_embeddings import vectorize
from classifier.pipelines.zero_shot import classifier

from db.services.hs_code_vector_service import get_nearest_neighbors


def item_to_text(item):
    """
    Convert an item object into a text string to classify.
    There is room to try various formatting options here to see what
    kinds of language features help the classifier.
    """
    s = "item is named {:s}.".format(item["name"])
    if item.get("categories"):
        s += " {:s} belongs to the category {:s}.".format(
            item["name"], item["categories"][0]
        )

    if item["description"] is not None:
        s += " {:s} is described by {:s}.".format(
            item["name"], item["description"]
        )
    return s


def classify(
    db: Session,
    item: Item,
    config: Config,
):
    """Vectorize an item and find the N most similar items"""
    vector = vectorize(item_to_text(item))

    top_n = get_nearest_neighbors(
        db=db, hierarchy=config.hierarchy, vector=vector, n=5
    )

    # print([item_to_text(item) for confidence, item in top_n])

    # use the zero shot classifier to sort the top N
    # results by similarity
    result = classifier(
        item_to_text(item),
        [item_to_text(item.__dict__) for confidence, item in top_n],
    )

    # Extract scores from the result
    scores = result["scores"]

    # Combine scores with items
    combined = list(zip(top_n, scores))

    # Sort by scores in descending order
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)

    # Separate items and scores again
    sorted_top_n, sorted_scores = zip(*sorted_combined)

    return [
        Classification(
            name=item.name,
            description=item.description,
            hierarchy=item.hierarchy.name,
            confidence=score,
        )
        for (confidence, item), score in zip(sorted_top_n, sorted_scores)
    ]
