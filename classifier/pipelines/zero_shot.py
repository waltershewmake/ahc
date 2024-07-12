"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 07-11-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

from transformers import pipeline

#
# Switch the zero-shot classifier model here.
# Note: The model will take time to download the first time it is used.
# Be patient. There may not be any output from the Docker container for a while.
#
which_model = 0
models = [
    "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",  # 0
    "MoritzLaurer/DeBERTa-v3-large-zeroshot-v1.1-all-33",  # 1
    "MoritzLaurer/DeBERTa-v3-base-mnli-xnli",  # 2
    "facebook/bart-large-mnli",  # 3
    "knowledgator/comprehend_it-base",
]  # 4
classifier = pipeline("zero-shot-classification", model=models[which_model])
