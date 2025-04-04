# **ECS Directory - Terraform Configuration**

This directory contains Terraform scripts to create and manage an AWS ECS (Elastic Container Service) cluster. It includes:

- `main.tf`: The main Terraform script to define and create the ECS cluster and related resources.
- `variables.tf`: A file that defines the variables used in the Terraform configuration.

## **Variables**

The `variables.tf` file defines several variables used for configuring the ECS cluster. Some of these variables have default values, but others must be defined in the `terraform.tfvars` file for Terraform to run successfully. Only variables without default values are essential and must be included in the `terraform.tfvars` file.

Below is a list of all the variables in `variables.tf`:

#### **1. REGION**
- **Description**: Desired AWS region where the ECS cluster is located.
- **Type**: `string`
- **Default**: `"eu-west-2"`

#### **2. VPC_ID**
- **Description**: The VPC where the ECS cluster will be deployed.
- **Type**: `string`
- **Default**: `"vpc-0f7ba8057a52dd82d"`

#### **3. DB_PORT**
- **Description**: The port number to connect to the RDS database.
- **Type**: `string`
- **Default**: `"1433"`

#### **4. DB_DRIVER**
- **Description**: The database driver for SQL Server.
- **Type**: `string`
- **Default**: `"ODBC Driver 18 for SQL Server"`

#### **5. DB_USERNAME**
- **Description**: The username for the RDS database.
- **Type**: `string`

#### **6. DB_PASSWORD**
- **Description**: The password for the RDS database.
- **Type**: `string`

#### **7. DB_NAME**
- **Description**: The SQL Server database name.
- **Type**: `string`

#### **8. DB_HOST**
- **Description**: The RDS endpoint.
- **Type**: `string`

#### **9. AWS_SECRET_KEY**
- **Description**: The AWS secret key for authentication.
- **Type**: `string`

#### **10. AWS_ACCESS_KEY**
- **Description**: The AWS access key for authentication.
- **Type**: `string`

#### **11. DASHBOARD_ECR**
- **Description**: The ECR repository name for the dashboard container.
- **Type**: `string`
- **Default**: `"c16-trenet-dashboard-ecr"`

#### **12. DASHBOARD_ECR_IMAGE**
- **Description**: The specific image to use from the ECR repository.
- **Type**: `string`

#### **13. ECS_TASK_DEF**
- **Description**: The ECS task definition name.
- **Type**: `string`
- **Default**: `"c16-trenet-task-def-ecs"`

#### **14. ECS_SERVICE**
- **Description**: The ECS service name.
- **Type**: `string`
- **Default**: `"c16-trenet-service-ecs"`

#### **15. ECS_CLUSTER**
- **Description**: The ECS cluster name.
- **Type**: `string`
- **Default**: `"c16-ecs-cluster"`

#### **16. SUBNET1, SUBNET2, SUBNET3**
- **Description**: The subnet IDs for the ECS cluster deployment.
- **Type**: `string`

#### **17. SG_NAME**
- **Description**: The security group name for ECS.
- **Type**: `string`
- **Default**: `"c16-trenet-ecs-sg"`

#### **18. EXECUTION_ROLE_ARN**
- **Description**: The IAM execution role ARN for ECS task definition.
- **Type**: `string`
- **Default**: `"arn:aws:iam::129033205317:role/ecsTaskExecutionRole"`

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
