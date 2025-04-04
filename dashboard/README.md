# Plant Health Monitoring Dashboard

## Overview
This Streamlit dashboard provides real-time insights into the health of plants in the Liverpool Museum of Natural History (LMNH) botanical wing. The dashboard displays sensor data, including temperature, soil moisture, and watering times, while also generating alerts for extreme temperatures and low moisture levels.

## Features
- Displays real-time **temperature** and **soil moisture** data for each plant.
- Shows the **last watered timestamp** for each plant.
- Generates **alerts** for:
  - Extreme temperature conditions.
  - Low soil moisture levels.
- Connects to a temporary database that maintains **only the last 24 hours** of data.

## Installation & Setup

### Environment Variables
Create a `.env` file in the project root with the following variables:

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
```

### Install Dependencies
Install the required Python packages using:

```
pip install -r requirements.txt
```

### Run the Dashboard
Start the Streamlit application using:

```
streamlit run dashboard.py
```

## Docker Deployment
The project includes a `Dockerfile` for containerized deployment.

### Build the Docker Image
```
docker build -t plant-health-dashboard .
```

### Run the Docker Container
```
docker run -p 8501:8501 --env-file .env plant-health-dashboard
```

## Directory Structure
```
/dashboard
│-- dashboard.py        # Streamlit dashboard application
│-- models.py           # Database models and data handling
│-- requirements.txt    # Python dependencies
│-- Dockerfile          # Docker configuration
│-- .env.example        # Example environment variables file
```

