# **EventBridge Directory - Terraform Configuration**

This directory contains Terraform scripts to create and manage AWS EventBridge schedules. It includes:

- `main.tf`: The main Terraform script to define and create the EventBridge schedules.
- `variables.tf`: A file that defines the variables used in the Terraform configuration.

## **Variables**

The `variables.tf` file defines several variables used for configuring the EventBridge schedules. Some of these variables have default values, but others must be defined in the `terraform.tfvars` file for Terraform to run successfully. Only variables without default values are essential and must be included in the `terraform.tfvars` file.

Below is a list of all the variables in `variables.tf`:

#### **1. REGION**
- **Description**: Desired AWS region.
- **Type**: `string`
- **Default**: `"eu-west-2"`

#### **2. LAMBDA_NAME1**
- **Description**: Name of the Lambda function used for pipeline 1.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline1-lambda"`

#### **3. LAMBDA_NAME2**
- **Description**: Name of the Lambda function used for pipeline 2.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline2-lambda"`

#### **4. PIPELINE1_SCHEDULE_NAME**
- **Description**: EventBridge schedule name for pipeline 1.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline1_scheduled_event"`

#### **5. PIPELINE2_SCHEDULE_NAME**
- **Description**: EventBridge schedule name for pipeline 2.
- **Type**: `string`
- **Default**: `"c16-trenet-pipeline2_scheduled_event"`

#### **6. SCHEDULE1_TRIGGER_RATE**
- **Description**: EventBridge schedule trigger frequency for pipeline 1.
- **Type**: `string`
- **Default**: `"rate(1 minute)"`

#### **7. SCHEDULE2_TRIGGER_RATE**
- **Description**: EventBridge schedule trigger frequency for pipeline 2.
- **Type**: `string`
- **Default**: `"rate(1 hour)"`

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
