# Storing Plant records for the Liverpool Natural History Museum

This project aims to help the Liverpool Natural History Museum (LNMH) monitor the health of their plants in their new botanical wing which will display and showcase the diversity of plant life in the region and the important roles plant life plays in our daily lives. The museum has a large number of plants and are looking for a way to monitor the health of plants and alert gardeners when there is a problem with the plants.
LMNH has an API setup already which returns sensor data from the plants as well as other useful data about the plant such as its name, species and the gardener looking after it. These are updated every minute.

Costs are a major factor so LNMH wants to use a temporary short term database that stores the last 24 hours of plant data only, older data should be removed and archived. The cost being a restriction has influenced many of the decisions in the project the most important of these being the cloud resources that we have used. Decisions such as using Lambda's instead of EC2 instances and the use of S3 buckets have been made to minimize the cost of the architecture. A dashboard was created, using the data in the RDS, where visualizations and alerts were set up to notify gardeners when a plant needs attention.

This repository contains Infrastructure as Code (IaC) scripts to provision cloud resources on AWS using terraform and data pipelines to manage plant record data on AWS. It provisions cloud resources using Terraform and includes two data processing pipelines deployed as AWS Lambda functions.

## Directory Structure

The following subdirectories contain scripts for each major component of this project. These components are creating the cloud and database architecture in `/architecture`, requesting the API and inserting request data as rows into RDS in `/data-pipeline-1`, deleting the 24 hour old data from the RDS and uploading it onto an S3 bucket as a CSV in `/data-pipeline-2` and creating a dashboard of the data in the RDS in `/dashboard`.

### **1. Architecture**

The [`architecture/`](architecture/) directory contains Terraform scripts to provision AWS resources (such as the Lambda's, RDS and S3), the RDS database schema and the cloud architecture diagram.
For details, see [Architecture README](architecture/README.md).

---

### **2. Data Pipeline 1: Data Ingestion**

The [`datapipeline1/`](datapipeline1/) directory contains scripts to fetch, clean, and store plant records in RDS. It also contains scripts to dockerize this pipeline and run it on an AWS Lambda.
For more details, refer to the [Data Pipeline 1 README](data-pipeline-1/README.md).

---

### **3. Data Pipeline 2: Data Archiving**

The [`datapipeline2/`](datapipeline2/) directory archives 24-hour-old data to S3 and removes the archived data from the RDS. It also contains scripts to dockerize this pipeline and run it on an AWS Lambda.
For more details, refer to the [Data Pipeline 2 README](data-pipeline-2/README.md).

---

### **4. Dashboard**

The [`dashboard/`](dashboard/) directory contains the scripts to run a `streamlit` dashboard that botanists can interact with to see the status of different plants.
For more details, refer to the [Dashboard README](dashboard/README.md).

The current deployed dashboard can be accessed through the following link: `http://18.168.203.70:8501/`