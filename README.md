<!--
Author: Walter Shewmake <walter.shewmake@utahtech.edu>
Date: 05-19-2024

Project: Arbitrary Hierarchical Classifier
Client: Zonos
Affiliation: Utah Tech University

This file is part of the Arbitrary Hierarchical Classification Application developed for Zonos.
-->

# FastAPI Classifier on AWS with PostgreSQL

[Setup](#setup) | [Prerequisites](#prerequisites) | [Steps](#steps) | [Parsing Hierarchical Data](#parsing-hierarchical-data) | [Profiling Results](#profiling-results) | [Accuracy](#accuracy) | [Cost Analysis](#cost-analysis) | [Conclusion](#conclusion)

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

## Setup environment

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

## Parsing a file

1. Note the hierarchy type and file structure, and determine if one of the existing transformers can be used (see `file_parser/transformers`).
2. If it can, prefix the file name with the hierarchy in all caps, for example, "**UN_SPSC**\_1.csv" If there is no existing transformer capable of parsing the file, you'll need to [create a transformer](#create-a-transformer).
3. Run the file parser using the following command:
   ```bash
   python -m file_parser <file_path>
   ```

## Create a transformer

The BaseTransformer class was created with flexibility and future expansion in mind, so it should be easy to extend. To create a new transformer, follow these steps:

1. Create a new file in `file_parser/transformers` named after your hierarchy.
2. Create a new transformer class that inherits from `BaseTransformer`.
3. Add the hierarchy and transformer names to the class attributes `__hierarchy__` and `__transformer__`.
   - The `__hierarchy__` attribute is used to associate the transformer with one of the hierarchies defined in the database.
   - The `__transformer__` attribute is used to identify the transformer in the file parser.
4. Implement the `parse` method to read the file and transform the data into a list of dictionaries. There are three required fields:
   - `name`: The unique identifier for the hierarchy item.
   - `parent_name`: The unique identifier for the parent item.
   - `desc`: A description of the item used for classification.
5. Call the `try_import` method with the list of dictionaries to import the data into the database.
6. Add your hierarchy to the `HierarchyType` enum in `api/schemas.py`.

### Example Transformer

```python
# file_parser/transformers/YOUR_TRANSFORMER.py

import csv
from file_parser.base import BaseTransformer


class YOUR_TRANSFORMER(BaseTransformer):
   """
   YOUR_TRANSFORMER Transformer

   part_id -> name
   parent_id -> parent_name
   eccn_desc -> desc
   """

   __hierarchy__ = "YOUR_HIERARCHY"
   __transformer__ = "YOUR_TRANSFORMER"

   def parse(self):
      """Parse a file"""
      if not super().parse():
            return

      rows = []
      with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
               parsed_row = {
                  "name": row.get("part_id").strip(),
                  "parent_name": row.get("parent_id").strip(),
                  "desc": row.get("eccn_desc"),
               }
               rows.append(parsed_row)

      if not rows:
            print("No rows to import")
            return

      # Import the data
      self.try_import(rows)
```

# Profiling Results

### Setup

- **DB**: AWS RDS PostgreSQL `db.t3.xlarge` (peaked at 22% CPU, could probably get away with a t3.small)
- **EB**: Python 3.9 running on 64bit Amazon Linux 2023/4.0.12
- **EC2**: Seven `t3.micro` instances running behind a load balancer (each capable of 7-12 RPS, so you could get away with five instances for 50 RPS)
- **Classifier**: OpenAI `text-embedding-3-large`

### Usage

- **DB**: Peaked at `22%` CPU usage
- **EB**: Peaked at `15%` CPU usage avg. across all instances
- **Classifier**: Peaked at `49.5` RPS (99% of OpenAI's tier 1 limit)

### Results

![aws eb health](aws_eb_health.png)
![request statistics 1](request_statistics_1.png)
![request statistics 2](request_statistics_2.png)

### Proof of RPS > 10 per worker

![peak rps per worker](peak_rps_per_worker.png)

### Observations

After increasing the number of users from 20 to 21, the RPS began to drop off, likely due to the classifier reaching the OpenAI tier 1 limit. The CPU usage on the EB instances remained low, so the bottleneck is likely OpenAI. The RDS instance was able to handle the load without issue, so the next step would be to upgrade the OpenAI plan to increase the RPS limit, and then continue to increase the number of users until the CPU usage maxes out on the EB instances or the RDS instance.

# Accuracy

## Chart 1

## Description

A histogram representing 6000 demo items randomly sampled from a Taxonomy dataset that shows (in blue) the distribution of the cosine distances between the correct leaf node (`y`) in the hierarchy and the leaf node identified by the classifier (`ŷ`), and (in orange) the distribution of the cosine distances between the correct leaf node (`y`) and the randomly selected leaf node (`ŷ_rand`). 6000 classifications were made in total, and 6000 random leaf nodes were selected.

![chart 1 log scale](chart_1_log.png)

### Observations

- The median cosine distance between `y` and `ŷ` is ..., indicating that the classifier is able to identify the correct leaf node in the hierarchy with high accuracy.
- The median cosine distance between `y` and `ŷ_rand` is ..., indicating that randomly selected leaf nodes are far from the correct leaf node in the hierarchy.

## Chart 2

## Description

A histogram that shows (in blue) the distribution of the cosine distances between the correct leaf node (`y`) in the hierarchy and generated embedding of the input item (`v`).

![chart 2 log scale](chart_2_log.png)

# Cost Analysis

## OpenAI Costs

`10,778` requests were made, putting the total cost from openAI at about `$0.20`. This cannot be calculated exactly since we don't know the token amount, but I performed the following calculation to get a good estimate:

`5,536,446` tokens used for the day / `39,403` requests made for the day \* `10,778` requests in the test = `1,514,397.7612872116` tokens used in the test

`text-embedding-3-large` price: `$0.13/million tokens`

Total cost: `1,514,397.7612872116` / `1,000,000` \* `0.13` = `$0.196871709` (about `$0.20`)

## AWS Costs

The total AWS cost for the day was `$1.09`. The majority of the cost was due to the RDS instance, which was `$0.94`.

![aws cost](aws_cost.png)

## Total Cost

The total cost for the day was `$1.29`, putting the cost per request at about `$0.0001196883`, which is an overestimate since the classifier was only used for a fraction of the day, but we included the AWS costs for the entire day.

# Conclusion

Initial product requirements:

## Database

- [x] All hierarchies shall be stored identically in a Postgres database
- [x] Relevant database hierarchies shall be retrieved from the database at the time of request, adhering to the principles of minimal retrieval

## Application

- [x] API shall be a FastAPI
- [x] API shall be either REST or GraphQL
- [x] Accepts item information similar to the `ClassificationCalculateInput` schema here, with an added field (enum) specifying the classification hierarchy (i.e. UNSPSC, US_ECCN, etc):
      https://zonos.com/developer/types/ClassificationCalculateInput

### Returns

- [x] The top 5 most likely classifications and their corresponding probabilities
- [x] P95 response times shall be < 1 sec
- [x] Concurrency per worker shall be > 10 simultaneous requests
- [x] Cost per request shall be < $0.01

## Hierarchies

- [x] US Product Tax Codes (US_PTC)
- [x] US Export Control Classification Numbers (US_ECCN)
- [x] UN Commodity Codes (UN_SPSC)
- [x] EU DUal Use Codes (EU_ECCN)

```

```
