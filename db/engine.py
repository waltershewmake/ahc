"""
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-08-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This module is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
"""

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

RDS_DB_NAME = os.getenv("RDS_DB_NAME")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
RDS_PORT = os.getenv("RDS_PORT")

engine = create_engine(
    f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"
)
