# **Lambda Directory - Terraform Configuration**

This directory contains Terraform scripts to create and manage AWS Lambda functions. It includes:

- `main.tf`: The main Terraform script to define and create the Lambda functions.
- `variables.tf`: A file that defines the variables used in the Terraform configuration.

## **Variables**

The `variables.tf` file defines several variables used for configuring the Lambda functions. Some of these variables have default values, but others must be defined in the `terraform.tfvars` file for Terraform to run successfully. Only variables without default values are essential and must be included in the `terraform.tfvars` file.

Below is a list of all the variables in `variables.tf`:

#### **1. REGION**
- **Description**: Desired AWS region where the Lambdas are deployed.
- **Type**: `string`
- **Default**: `"eu-west-2"`

#### **2. VPC_ID**
- **Description**: The VPC where the Lambda functions will be deployed.
- **Type**: `string`
- **Default**: `"vpc-0f7ba8057a52dd82d"`

#### **3. PIPELINE1_ECR**
- **Description**: Name of the ECR repository for pipeline 1.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline1-ecr"`

#### **4. PIPELINE2_ECR**
- **Description**: Name of the ECR repository for pipeline 2.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline2-ecr"`

#### **5. LAMBDA_NAME1**
- **Description**: Name of the Lambda function for pipeline 1.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline1-lambda"`

#### **6. LAMBDA_NAME2**
- **Description**: Name of the Lambda function for pipeline 2.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline2-lambda"`

#### **7. DB_PORT**
- **Description**: The port number to connect to the RDS database.
- **Type**: `number`
- **Default**: `1433`

#### **8. DB_DRIVER**
- **Description**: The driver used to connect to the database.
- **Type**: `string`
- **Default**: `"ODBC Driver 18 for SQL Server"`

#### **9. DB_USERNAME**
- **Description**: The username for connecting to the RDS database.
- **Type**: `string`

#### **10. DB_PASSWORD**
- **Description**: The password for connecting to the RDS database.
- **Type**: `string`

#### **11. DB_NAME**
- **Description**: The name of the SQL Server database.
- **Type**: `string`

#### **12. AWS_SECRET_KEY**
- **Description**: The user's AWS secret key.
- **Type**: `string`

#### **13. AWS_ACCESS_KEY**
- **Description**: The user's AWS access key.
- **Type**: `string`

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
