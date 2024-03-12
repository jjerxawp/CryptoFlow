# CryptoFlow

"CryptoFlow" is a demonstration project illustrating the integration of diverse technologies to process cryptocurrency data seamlessly. 

Through the utilization of **Scrapy**, it gathers information from various cryptocurrency APIs, which is subsequently channeled to a Spark cluster via Kafka for streamlined processing. Airflow serves as the orchestration tool, managing the entire workflow. 

Leveraging **Docker**, deployment of key components such as **Airflow**, **Spark**, **MongoDB**, and **Kafka** is simplified. This project offers a tangible example of real-time cryptocurrency data processing for analytical insights.
## Overview
"CryptoFlow" is a demonstration project showcasing the seamless integration of various technologies for cryptocurrency data processing.

This project serves as a practical example for how real-time cryptocurrency data can be captured and transformed for analytics.

## Overall Architecture
![CryptoFlow-Architecture](https://private-user-images.githubusercontent.com/91967861/311942118-fa411aad-21fb-4ea6-91ab-9e7866588351.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTAyMTg1MDQsIm5iZiI6MTcxMDIxODIwNCwicGF0aCI6Ii85MTk2Nzg2MS8zMTE5NDIxMTgtZmE0MTFhYWQtMjFmYi00ZWE2LTkxYWItOWU3ODY2NTg4MzUxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDAzMTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwMzEyVDA0MzY0NFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWVjZTRiM2UwNzE5NzNiMmZhNmEzMmRkNzBjYWUyMGZhOTkyMDcwZTk3NWFkMWZhZTc3MWU0ZWEyZGYyMGIxYzUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.8iImjTnmu_skBmPSSHLUYRPvRqZpzjHYoSdqZQJfiVk)

In the Docker environment, our stack comprises Airflow running in Celery executor mode, using Postgres as backend and Redis as a queue system for task management. 

Additionally, Kafka is employed in a single Kafka single Zookeeper configuration to offload work, serving as a reliable messaging system (can easily scale out by adding more Kafka server to the docker compose file). 

As this is a demonstration project, a standalone Spark cluster is utilized for data processing, omitting Hadoop for simplicity. Besides, you can also easily scale out by adding more worker in the docker compose file. 

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


