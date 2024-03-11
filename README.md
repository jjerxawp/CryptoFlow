# CryptoFlow

"CryptoFlow" is a demonstration project illustrating the integration of diverse technologies to process cryptocurrency data seamlessly. 

Through the utilization of **Scrapy**, it gathers information from various cryptocurrency APIs, which is subsequently channeled to a Spark cluster via Kafka for streamlined processing. Airflow serves as the orchestration tool, managing the entire workflow. 

Leveraging **Docker**, deployment of key components such as **Airflow**, **Spark**, **MongoDB**, and **Kafka** is simplified. This project offers a tangible example of real-time cryptocurrency data processing for analytical insights.
## Overview
"CryptoFlow" is a demonstration project showcasing the seamless integration of various technologies for cryptocurrency data processing.

This project serves as a practical example for how real-time cryptocurrency data can be captured and transformed for analytics.

## Overall Architecture
![CryptoFlow-Architecture](https://private-user-images.githubusercontent.com/91967861/311826037-cdc1e338-10b9-4c35-89d9-0b3fbf0303f1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTAxODIxMzAsIm5iZiI6MTcxMDE4MTgzMCwicGF0aCI6Ii85MTk2Nzg2MS8zMTE4MjYwMzctY2RjMWUzMzgtMTBiOS00YzM1LTg5ZDktMGIzZmJmMDMwM2YxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzExVDE4MzAzMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTZlNzdiNTQ5MDE3OTA3Y2U3Yjg0NzllMWMzYzUzYzZjMzUwNjRlZjY1MWU5NGIyZDhkZjc1YWZmYmQ5YmRhYzAmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.74s6Yf-QOfYliEBJwDimHvQIARAvKIJttNcz_AUa2QI)

In the Docker environment, our stack comprises Airflow running in Celery executor mode, leveraging Postgres and Redis as a queue for task management. 

Additionally, Kafka is employed in a single Kafka single Zoo configuration to offload work, serving as a reliable messaging system. 

As this is a demonstration project, a standalone Spark cluster is utilized for data processing, omitting Hadoop for simplicity. 

Once processed, data is dumped into MongoDB for storage and further analysis. 

This setup ensures seamless orchestration of tasks, efficient message queuing, and robust data processing capabilities, making it ideal for showcasing real-time cryptocurrency data analytics.

## Features

- **Data Collection:** Utilizes Scrapy to collect data from cryptocurrency APIs.
- **Data Processing:** Delivers collected data to a Spark cluster via Kafka for efficient processing.
- **Workflow Orchestration:** Airflow orchestrates the entire data processing workflow.
- **Containerized Deployment:** Docker facilitates easy deployment of components including Airflow, Spark, MongoDB, and Kafka.

## Installation

*Ensure Docker is installed on your system before running the provided commands. Adjust any configuration settings as needed before deployment.*

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/CryptoFlow.git

2. Navigate to the project directory:

   ```bash
   cd CryptoFlow
3. Define the required environment variable, you can use default setup by rename the .env-sample file:
   ```bash
   mv .env-sample .env

4. Build the image for later running Spark clusters (standalone version, without Hadoop)

   ```bash
   docker build -t cluster-apache-spark:3.0.2 -f ./spark-cluster/Dockerfile .
5. Run the compose file to spin up the entire stack:
   ```bash
   docker compose -f cryptoflow-compose-file.yml up -d
6. Open your browser and navigate to localhost:8080 to access Airflow and log in.


