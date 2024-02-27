from pyspark import SparkConf
from pyspark.sql import SparkSession, Window
from pyspark.sql.types import *
from pyspark.sql.functions import *
import os
import sys
import pandas as pd
import csv
import json
import datetime


if __name__ == "__main__":

    topic                   = "lists"
    spark_app_name          = "spark_coingecko_lists"
    broker                  = "kafka:9092"
    mongodb_database        = "coingecko"
    mongodb_collection      = "lists"

    os.environ['PYSPARK_PYTHON']        = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    conf = SparkConf() \
        .setAppName(spark_app_name) \
        .setMaster("spark://spark-master:7077") \
        .set("spark.sql.legacy.timeParserPolicy", "LEGACY") \
        .set("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.2") \
        .set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.2") \
        .set("spark.mongodb.write.connection.uri", "mongodb://root:root@mongodb:27017/") \
        .set("spark.streaming.stopGracefullyOnShutdown", "true")

    spark = SparkSession \
        .builder \
        .config(conf=conf) \
        .getOrCreate()

    raw_lists_df = spark.read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", broker) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()

    schema_coingecko_list_api = StructType([
        StructField("gecko_id", StringType(), nullable=False),
        StructField("symbol", StringType(), nullable=False),
        StructField("name", StringType(), nullable=False),
        StructField("platforms", MapType(StringType(), StringType()), nullable=True)
    ])

    value_df = raw_lists_df.select(
        from_json(col("value")
                  .cast("string"), schema=schema_coingecko_list_api)
        .alias("value")
    )

    cleansed_df = value_df.select("value.*")

    cleansed_df.printSchema()
    cleansed_df.show(5, truncate=False)

    write_df = cleansed_df.write \
        .format("mongo") \
        .mode("append") \
        .option("database", mongodb_database) \
        .option("collection", mongodb_collection) \
        .option("uri","mongodb://root:root@mongodb:27017/") \
        .save()