<!--
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-19-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This file is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
-->

# FastAPI Classifier on AWS with PostgreSQL

[Setup](#setup) | [Prerequisites](#prerequisites) | [Steps](#steps) | [Parsing Hierarchical Data](#parsing-hierarchical-data)

# Setup

This guide outlines the steps required to set up an AWS environment to run the FastAPI classifier application with a PostgreSQL database using Elastic Beanstalk and RDS.

## Prerequisites

- AWS account
- AWS CLI installed and configured
- Elastic Beanstalk CLI (EB CLI) installed
- AWS IAM user with necessary permissions

## Steps

1. `brew install awsebcli` or `pip install awsebcli`
2. `eb init` and follow the prompts
3. `eb create` and follow the prompts
4. `eb console` to open the console in a browser
5. Create an RDS instance in the same VPC as the Elastic Beanstalk environment
6. Enable the pgvector extension on the RDS instance by connecting to the database and running the following command:
   ```sql
   CREATE EXTENSION vector;
   ```
7. Add the following environment variables to the Elastic Beanstalk environment:
   ```env
   OPENAI_API_KEY=<your_openai_api_key>
   ```
8. `eb deploy` to deploy the application

# Parsing Hierarchical Data

The classifier expects a uniform data format in order to provide accurate predictions. There is no mechanism for automatically inserting files into the database on deployment, so you'll need to connect to the remote database from your local machine. The following steps outline how to parse hierarchical data into a format suitable for the classifier:

1. Create a `.env` file in the root directory of the project and add the following environment variables:
   ```env
   RDS_DB_NAME=<your_db_name>
   RDS_USERNAME=<your_db_username>
   RDS_PASSWORD=<your_db_password>
   RDS_HOSTNAME=<your_db_hostname>
   RDS_PORT=<your_db_port>
   OPENAI_API_KEY=<your_openai_api_key>
   ```
2. Create a python virtual environment and install the required dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Note the hierarchy type and file structure, and determine if one of the existing transformers can be used (see `file_parser/transformers`). If it can, prefix the file name with the hierarchy in all caps, for example, UN_SPSC_1.csv" If there is no existing transformer capable of parsing the file, create a new transformer class that inherits from `BaseTransformer` and implements the `parse` method. The BaseTransformer class was created with flexibility and future expansion in mind, so it should be easy to extend. The transformer should be placed in the `file_parser/transformers` directory.
4. Run the file parser using the following command:
   ```bash
   python -m file_parser <file_path>
   ```
