from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor

import io
from datetime import datetime, timedelta
import os
import requests
import zipfile
import warnings
from sys import stdout
from os import makedirs
from os.path import dirname
from os.path import exists

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

packages = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.2,"

dag = DAG(
    "coingecko_job",
    default_args=default_args,
    start_date=datetime(2023, 12, 1),
    schedule_interval='@once',
    catchup=False
)

start = DummyOperator(
    task_id="start",
    dag=dag
)

server_check = HttpSensor(
    task_id="server_check",
    http_conn_id="coingecko_conn",
    endpoint="ping",
    method="GET",
    response_check=lambda response: response.json(
    )["gecko_says"] == "(V3) To the Moon!"
)

crawling_markets = BashOperator(
    task_id="crawling_markets",
    trigger_rule="all_success",
    bash_command="cd /usr/local/airflow/scrapy/crypto/ && scrapy crawl coingecko-markets"
)
crawling_lists = BashOperator(
    task_id="crawling_lists",
    trigger_rule="all_success",
    bash_command="cd /usr/local/airflow/scrapy/crypto/ && scrapy crawl coingecko-lists"
)

spark_coingecko_coin_markets = SparkSubmitOperator(
    task_id="spark_coingecko_coin_markets",
    conn_id="spark_default",
    application="/usr/local/spark_data/apps/spark_coingecko_markets.py",
    packages=packages,
    verbose=1,
    trigger_rule="all_success",
    dag=dag
)

spark_coingecko_coin_lists = SparkSubmitOperator(
    task_id="spark_coingecko_coin_lists",
    conn_id="spark_default",
    application="/usr/local/spark_data/apps/spark_coingecko_lists.py",
    packages=packages,
    verbose=1,
    trigger_rule="all_success",
    dag=dag
)

end = DummyOperator(
    task_id="end",
    trigger_rule='all_success',
    dag=dag
)

start >> server_check >> [crawling_markets, crawling_lists]
crawling_markets >> spark_coingecko_coin_markets >> end
crawling_lists >> spark_coingecko_coin_lists >> end

# start >> server_check >> crawling_markets >> spark_coingecko_coin_markets >> end