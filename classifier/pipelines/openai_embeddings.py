"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


WHICH_MODEL = 1
models = ["text-embedding-3-small", "text-embedding-3-large"]
print(f"Using model: {models[WHICH_MODEL]}")
embeddings = OpenAIEmbeddings(model=models[WHICH_MODEL])


def vectorize(text: str) -> list[float]:
    """Vectorize a text string"""

    return embeddings.embed_query(text)


def bulk_vectorize(texts: list[str]) -> list[list[float]]:
    """Vectorize a list of text strings"""

    return embeddings.embed_documents(texts)


async def vectorize_async(text: str) -> list[float]:
    """Vectorize a text string"""

    return await embeddings.aembed_query(text)
