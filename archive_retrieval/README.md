# Archive Retrieval

This directory contains Python scripts that allow a user to retrieve archived data by running a script with two command line inputs, the start date and the end date, which then queries the Athena database. Athena outputs the query result in an S3 bucket. This result is then downloaded from the S3 bucket and stored locally as `requested_data.csv`. It includes:

- `athena_manager.py`: Manages interactions with the Athena database via the `AthenaHandler` object. This object creates a `boto3` Athena client on instantiation. `AthenaHandler` has the method `query_athena` which queries the Athena table and downloads the result to the S3 bucket.

- `s3_athena_manager.py`: Manages interactions with the S3 bucket which stores the result of the Athena queries. This is done by the class `S3AthenaManager`. On instantiation it creates a `boto3` S3 client. The method `download_athena_data` can then be used to download the CSV which was uploaded by Athena.

- `cli.py`: This contains the command line tool for running these tasks. It uses the `AthenaHandler` and `S3AthenaManager` objects to interact with Athena and S3. It takes two inputs by command line which corresponding to start and end timestamp for filtering.

- `requirements.txt`: Lists all Python dependencies required to run the pipeline and the appropriate tests.
---

## **Environment Variables**

Certain environment variables are needed in a `.env` file for the pipeline to run locally or on the cloud. These variables are essential for setting up database connections, S3 access, and other pipeline-specific settings. Below is a list of the required environment variables:

#### **1. ACCESS_KEY_ID**
- **Description**: Your AWS access key.

#### **2. SECRET_ACCESS_KEY_ID**
- **Description**: Your AWS secret key.

#### **3. BUCKET_REGION**
- **Description**: AWS region where your S3 is located.

#### **4. DB_NAME_ATHENA**
- **Description**: Athena database name.

#### **5. S3_BUCKET_OUTPUT_LOCATION**
- **Description**: Location in an S3 bucket for the Athena query to output.

#### **6. S3_ATHENA_BUCKET_NAME**
- **Description**: Name of S3 bucket used to store Athena query outputs.

Ensure that all these environment variables are set in your environment or defined in a configuration file (like a `.env` file) before running the pipeline.

---

## **Required Configuration**

Before running the pipeline, make sure that all the necessary environment variables are defined on the cloud or locally. These are essential for the pipeline to connect to Athena and S3 bucket.

---
## **Steps to Run the CLI**

Note that both timestamps in the CLI should be in the format "YYYY-MM-DD HH:MM:SS"

1. **Create the .env**:

   python3 cli.py -st [start_timestamp_for_filter] -et [end_timestamp_for_filter]