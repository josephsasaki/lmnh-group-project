# **Athena Database - Terraform Configuration**

This directory contains Terraform scripts to create and manage an Athena database. It includes:

- `main.tf`: The main Terraform script to define and create the Athena database.
- `variables.tf`: A file that defines the variables used in the Terraform configuration.

## **Variables**

The `variables.tf` file defines several variables used for configuring the Athena database. Some of these variables have default values, but others must be defined in the `terraform.tfvars` file for Terraform to run successfully. Only variables without default values are essential and must be included in the `terraform.tfvars` file.

Below is a list of all the variables in `variables.tf`:

#### **1. ATHENA_BUCKET_NAME**
- **Description**: The name of the S3 bucket for Athena query results.
- **Type**: `string`
- **Default**: `"c16-trenet-athena-output-s3"`

#### **2. ATHENA_DB_NAME**
- **Description**: The name of the Athena database.
- **Type**: `string`
- **Default**: `"c16_trenet_athena_query_db"`

---

## **Required Configuration: terraform.tfvars**

The `terraform.tfvars` file is where you provide values for the variables that do not have a default. These are essential for the Terraform configuration to run successfully.

### How to create the `terraform.tfvars` file:

1. **Create a new file** in the same directory as your Terraform scripts, named `terraform.tfvars` by running the command `touch terraform.tfvars`.
2. **Provide values for the required variables** You can also override default values here if needed.

## **Steps to Run the Terraform Script**

1. **Initialize the Terraform working directory**:
   terraform init
   
2. **Apply the Terraform configuration**:

   terraform apply
   Provide confirmation i.e 'yes' when prompted with: Do you want to perform these actions?