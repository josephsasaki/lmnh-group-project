# Data Pipeline 2 - Data Archiver

This directory contains Python scripts that form Data Pipeline 2. The pipeline extracts 24-hour-old data from an RDS database, archives it as a CSV file in an S3 bucket, and then deletes these records from the RDS. It is designed to run within an AWS Lambda environment by containerizing required files using `Dockerfile`, uploading it to AWS ECR and then running this image through a AWS Lambda. It Includes:

- `rds_manager.py`: Manages interactions with the RDS database via the `RDSHandler` object. This object can establish and close the connection to the RDS, extract 24 hour old data from the RDS and delete rows from the RDS.

- `data_helper.py`: Contains the `DataHelper` object that contains utility functions for data manipulation. This includes saving the extracted data as a CSV file and Retrieving IDs of records that need to be deleted from the RDS.

- `s3_manager.py`: Handles interactions with Amazon S3 by using the `S3Manager` object. This includes creating an S3 client, generating a CSV file key for the S3 based on the current datetime and uploading the CSV file to the specified S3 bucket.

- `pipeline.py`: Instantiates the `RDSHandler`, `DataHelper` and `S3Manager` objects and orchestrates the entire data pipeline workflow by combining their methods into a single function called `run_archive_pipeline`.

- `lambda_handler.py`: Contains the AWS Lambda function that triggers the data pipeline process by calling the `run_archive_pipeline` function in `pipeline.py`.

- `requirements.txt`: Lists all Python dependencies required to run the pipeline and the appropriate tests.

- `Dockerfile`: Contains instructions for building a Docker image that packages the Lambda, installs dependencies, and executes the Lambda function.

- `test_rds_manager.py`: Contains testing script for `rds_manager.py`.

- `test_data_helper.py`: Contains testing script for `data_helper.py`.

- `test_s3_manager.py`: Contains testing script for `s3_manager.py`.

- `/tmp`: A directory that simulates the AWS Lambda environment’s temporary storage. The CSV file is saved here before being uploaded to S3.
---


## **Environment Variables**

Certain environment variables are needed in a `.env` file for the pipeline to run locally or on the cloud. These variables are essential for setting up database connections, S3 access, and other pipeline-specific settings. Below is a list of the required environment variables:

#### **1. ACCESS_KEY_ID**
- **Description**: Your AWS access key.

#### **2. SECRET_ACCESS_KEY_ID**
- **Description**: Your AWS secret key.

#### **3. BUCKET_REGION**
- **Description**: AWS region where your S3 is located.

#### **4. DB_HOST**
- **Description**: Hostname or endpoint of the RDS instance.

#### **5. DB_PORT**
- **Description**: Port number for the RDS instance.

#### **6. DB_USERNAME**
- **Description**: Username for connecting to the RDS.

#### **7. DB_PASSWORD**
- **Description**: Password for connecting to the RDS.

#### **8. DB_NAME**
- **Description**: Name of the database within the RDS instance.

#### **9. S3_BUCKET**
- **Description**: Name of the S3 bucket where the CSV file will be stored.

Ensure that all these environment variables are set in your environment or defined in a configuration file (like a `.env` file) before running the pipeline.

---

## **Required Configuration**

Before running the pipeline, make sure that all the necessary environment variables are defined on the cloud or locally. These are essential for the pipeline to connect to your RDS instance and S3 bucket.

---
## **Steps to Run the Lambda**
Note these steps should be given by AWS after creating an ECR but these have been included for completeness.

1. **Login to AWS CLI**:

   ```
   aws ecr get-login-password --region [REGION] | docker login --username AWS --password-stdin [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com
   ```

2. **Build Docker image**:

   ```
   docker build --platform="linux/amd64" --provenance=false -t [NAME_OF_ECR_REPO] .
   ```
   
3. **Tag Docker image**:

   ```
   docker tag [NAME_OF_EXR_REPO]:latest [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/[NAME_OF_EXR_REPO]:latest
   ```

4. **Push Docker image**:

   ```
   docker push [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/[NAME_OF_EXR_REPO]:latest
   ```

4. **Create Lambda and Test**:
    - Create the Lambda, select the image and test the output.