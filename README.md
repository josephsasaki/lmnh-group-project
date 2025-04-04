# AWS Data Pipeline with Terraform and Lambda

This repository contains Infrastructure as Code (IaC) scripts to provision cloud resources on AWS using terraform and data pipelines to manage plant record data on AWS. It provisions cloud resources using Terraform and includes two data processing pipelines deployed as AWS Lambda functions.

## Directory Structure

The following subdirectories contain scripts for each major component of this project. These components are creating the cloud and database architecture in `/architecture`, requesting the API and inserting request data as rows into RDS in `/data-pipeline-1`, deleting the 24 hour old data from the RDS and uploading it onto an S3 bucket as a CSV in `/data-pipeline-2` and creating a dashboard of the data in the RDS in `/dashboard`.

### **1. Architecture**

The [`architecture/`](architecture/) directory contains Terraform scripts to provision AWS resources (such as the Lambda's, RDS and S3), the RDS database schema and the cloud architecture diagram.
For details, see [Architecture README](architecture/README.md).


### **2. Data Pipeline 1: Data Ingestion**

The [`datapipeline1/`](datapipeline1/) directory contains scripts to fetch, clean, and store plant records in RDS. It also contains scripts to dockerize this pipeline and run it on an AWS Lambda.
For more details, refer to the [Data Pipeline 1 README](data-pipeline-1/README.md).

---

### **3. Data Pipeline 2: Data Archiving**

The [`datapipeline2/`](datapipeline2/) directory archives 24-hour-old data to S3 and removes the archived data from the RDS. It also contains scripts to dockerize this pipeline and run it on an AWS Lambda.
For more details, refer to the [Data Pipeline 2 README](data-pipeline-2/README.md).

---

### **3. Dashboard**

The [`dashboard/`](dashboard/) directory contains the scripts to run a `streamlit` dashboard that botanists can interact with to see the status of different plants.
For more details, refer to the [Dashboard README](dashboard/README.md).