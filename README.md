# CryptoFlow

"CryptoFlow" is a demonstration project illustrating the integration of diverse technologies to process cryptocurrency data seamlessly. 

Through the utilization of **Scrapy**, it gathers information from various cryptocurrency APIs, which is subsequently channeled to a Spark cluster via Kafka for streamlined processing. Airflow serves as the orchestration tool, managing the entire workflow. 

Leveraging **Docker**, deployment of key components such as **Airflow**, **Spark**, **MongoDB**, and **Kafka** is simplified. This project offers a tangible example of real-time cryptocurrency data processing for analytical insights.
## Overview
"CryptoFlow" is a demonstration project showcasing the seamless integration of various technologies for cryptocurrency data processing.

This project serves as a practical example for how real-time cryptocurrency data can be captured and transformed for analytics.

## Overall Architecture
![CryptoFlow-Architecture](https://github.com/jjerxawp/CryptoFlow/blob/main/CryptoFlow.jpg)

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


