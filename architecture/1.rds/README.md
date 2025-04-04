# **RDS Directory - Terraform Configuration**

This directory contains Terraform scripts to create and configure an AWS RDS instance with a SQL Server engine. It includes:

- `main.tf`: The main Terraform script to define and create the RDS instance.
- `variables.tf`: A file that defines the variables used in the Terraform configuration.
- `database/`: A directory with additional documentation on how to create and connect to the database.

## **Variables**

The `variables.tf` file defines several variables used for configuring the AWS RDS instance. Some of these variables have default values, but there are others that must be defined in the `terraform.tfvars` file for Terraform to successfully run. Only variables without default values are essential and must be included in the `terraform.tfvars` file.

Below is a list of all the variables in `variables.tf`:

#### **1. DB_USERNAME**
- **Description**: The username to connect to the RDS instance.
- **Type**: `string`
- **Default**: Not set (Required)

#### **2. DB_PASSWORD**
- **Description**: The password to connect to the RDS instance.
- **Type**: `string`
- **Default**: Not set (Required)

#### **3. REGION**
- **Description**: The AWS region where the RDS instance will be deployed.
- **Type**: `string`
- **Default**: `"eu-west-2"`

#### **4. VPC_ID**
- **Description**: The VPC ID where the RDS instance will be located.
- **Type**: `string`
- **Default**: `"vpc-0f7ba8057a52dd82d"`

#### **5. SG_NAME**
- **Description**: The name of the security group the RDS will be in.
- **Type**: `string`
- **Default**: `"c16-trenet-sg"`

#### **6. RDS_NAME**
- **Description**: The name of the RDS instance.
- **Type**: `string`
- **Default**: `"c16-trenet-sql-serv-rds"`

#### **7. RDS_SUBNET_GROUP_NAME**
- **Description**: The name of the subnet group for the RDS instance.
- **Type**: `string`
- **Default**: `"c16-public-subnet-group"`

---

## **Required Configuration: terraform.tfvars**

The `terraform.tfvars` file is where you provide values for the variables that do not have a default. These are essential for the Terraform configuration to run successfully.

### How to create the `terraform.tfvars` file:

1. **Create a new file** in the same directory as your Terraform scripts, named `terraform.tfvars` by running the command `touch terraform.tfvars`.
2. **Provide values for the required variables** (`DB_USERNAME`, `DB_PASSWORD`). You can also override other default values here if needed.

### Example `terraform.tfvars`:

DB_USERNAME = "my_db_username"
DB_PASSWORD = "my_db_password"

## **Steps to Run the Terraform Script**

1. **Initialize the Terraform working directory**:
   terraform init
   
2. **Apply the Terraform configuration**:
   terraform apply
   Provide confirmation i.e 'yes' when prompted with: Do you want to perform these actions?
