# Architecture

This directory contains Infrastructure as Code (IaC) scripts written in Terraform to provision and manage AWS cloud resources. Each service is configured in its respective directory.

## Directory Structure

The following subdirectories contain Terraform scripts for specific AWS services. Each subdirectory includes a `main.tf` script and a `variables.tf` file, the scripts should be run in the order they appear below:

### **1.RDS**  
[`1.rds/`](1.rds/) – Contains Terraform scripts to create and configure an AWS RDS instance with a SQL Server engine. Additionally, this directory also contains [`rds/database`](rds/database) which contains documentation of how to create and connect to the database.
For more details, refer to the [RDS README](rds/README.md).

### **2.S3**  
[`2.s3/`](2.s3/) – Contains Terraform scripts to create and manage an Amazon S3 bucket.  
For more details, refer to the [S3 README](s3/README.md).

### **3.ECR**  
[`3.ecr/`](3.ecr/) – Contains Terraform scripts to create and manage an AWS Elastic Container Registry (ECR) repository.  
For more details, refer to the [ECR README](ecr/README.md).

### **4.Lambda**  
[`4.lambda/`](4.lambda/) – Contains Terraform scripts to deploy an AWS Lambda function with associated IAM roles and permissions.  
For more details, refer to the [Lambda README](lambda/README.md).

### **5.EventBridge**  
[`5.eventbridge/`](5.eventbridge/) – Contains Terraform scripts to configure AWS EventBridge rules and event-driven workflows.  
For more details, refer to the [EventBridge README](eventbridge/README.md).

### **6.ECS**  
[`6.ecs/`](6.ecs/) – Contains Terraform scripts to provision an AWS Elastic Container Service (ECS) cluster and associated resources.  
For more details, refer to the [ECS README](ecs/README.md).