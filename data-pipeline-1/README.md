# Data Pipeline 1 - Pipeline Configuration

This directory contains Python scripts that form Data Pipeline 1. The pipeline extracts data from an API, transforms the JSON responses into `Plant` objects, and loads the data into a Microsoft SQL Server RDS. It is designed to run as an AWS Lambda function and can also be containerized using a `Dockerfile`, uploaded to AWS ECR, and then deployed as a Lambda function. It includes:

- `extract.py`: Defines the `RecordingAPIExtractor` class which uses multiprocessing to perform multiple API requests for retrieving plant records from the museum.

- `models.py`: Contains various classes for the which define a `Plant` object, which is also defined here. The `Plant` object is initialized with a JSON response from the API, this data is then used to initialize other objects which describe the JSON response in an OOP format such as a `Botanist` object to store a plants botanist. Each object defined has defined methods defined to clean its attributes.

- `transform.py`: Creates the `PlantRecordingFactory` class. When initialized with a list of JSON API responses, it converts them into cleaned `Plant` objects using the `produce_plant_objects` method.

- `load.py`: Implements the `DatabaseManager` class, which contains all necessary Microsoft SQL Server commands to insert data into the RDS. It is initialized with the list of plant objects obtained from `PlantRecordingFactory`. It utilizes the `load_all` method to load all the data stored in objects to the RDS.

- `test_extract.py`: Contains tests for `extract.py`.

- `test_transform.py`: Contains tests for `transform.py`.

- `test_load.py`: Contains tests for `load.py`.

- `test_models.py`: Contains tests for `models.py`.

- `pipeline.py`: Instantiates and orchestrates the `RecordingAPIExtractor` (extraction), `PlantRecordingFactory` (transformation), and `DatabaseManager` (loading) classes by running the `run_api_pipeline` function.

- `lambda_handler.py`: Contains the AWS Lambda function that triggers the pipeline process by calling `run_api_pipeline` from `pipeline.py`.

- `requirements.txt`: Lists all Python dependencies required to run the pipeline and its tests.

- `code_to_name.csv`: A utility file that maps country codes to country names.

- `Dockerfile`: Contains instructions for building a Docker image that packages the Lambda function, installs dependencies, and executes the handler.

---

## **Environment Variables**

Certain environment variables are needed in a `.env` file for the pipeline to run locally or on the cloud. These variables are essential for setting up API connections, database access, and other pipeline-specific settings. Below is a list of the required environment variables:

#### **1. DB_HOST**
- **Description**: Hostname or endpoint of the Microsoft SQL Server RDS.

#### **2. DB_PORT**
- **Description**: Port number for the RDS instance (commonly `1433`).

#### **3. DB_USERNAME**
- **Description**: Username for connecting to the RDS.

#### **4. DB_PASSWORD**
- **Description**: Password for connecting to the RDS.

#### **5. DB_NAME**
- **Description**: Name of the database within the RDS instance.

Ensure that all these environment variables are set in your environment or defined in a configuration file (like a `.env` file) before running the pipeline.

---

## **Required Configuration**

Before running the pipeline, make sure that all the necessary environment variables are defined on the cloud or locally. These are essential for the pipeline to connect to the API, RDS instance, and AWS services.

---

## **Steps to Run the Lambda**
Note these steps should be given by AWS after creating an ECR but these have been included for completeness.

1. **Login to AWS CLI**:

   aws ecr get-login-password --region [REGION] | docker login --username AWS --password-stdin [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com

2. **Build Docker image**:

   docker build --platform="linux/amd64" --provenance=false -t [NAME_OF_ECR_REPO] .
   
3. **Tag Docker image**:

   docker tag [NAME_OF_EXR_REPO]:latest [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/[NAME_OF_EXR_REPO]:latest

4. **Push Docker image**:

    docker push [AWS_ACCOUNT_ID].dkr.ecr.[REGION].amazonaws.com/[NAME_OF_EXR_REPO]:latest

4. **Create Lambda and Test**:
    - Create the Lambda, select the image and test the output.