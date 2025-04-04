# **S3 Directory - Terraform Configuration**

This directory contains Terraform scripts to create and manage an Amazon S3 bucket. It includes:

- `main.tf`: The main Terraform script to define and create the S3 bucket.
- `variables.tf`: A file that defines the variables used in the Terraform configuration.

## **Variables**

The `variables.tf` file defines several variables used for configuring the S3 bucket. Some of these variables have default values, but there are others that must be defined in the `terraform.tfvars` file for Terraform to successfully run. Only variables without default values are essential and must be included in the `terraform.tfvars` file.

Below is a list of all the variables in `variables.tf`:

#### **1. BUCKET_NAME**
- **Description**: The name of the S3 bucket.
- **Type**: `string`
- **Default**: `"c16-trenet-s3"`

#### **2. REGION**
- **Description**: The AWS region where the S3 bucket will be deployed.
- **Type**: `string`
- **Default**: `"eu-west-2"`

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
