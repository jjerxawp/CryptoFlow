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

    topic                   = "markets"
    spark_app_name          = "spark_coingecko_markets"
    broker                  = "kafka:9092"
    mongodb_database        = "coingecko"
    mongodb_collection      = "markets"

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

    raw_markets_df = spark.read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", broker) \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()

    raw_markets_df.show(5)

    schema_coingecko_markets_api = StructType([
        StructField('gecko_id', StringType()),
        StructField('symbol', StringType()),
        StructField('name', StringType()),
        StructField('current_price', DoubleType()),
        StructField('market_cap', DoubleType()),
        StructField('market_cap_rank', IntegerType()),
        StructField('fully_diluted_valuation', DoubleType()),
        StructField('total_volume', DoubleType()),
        StructField('high_24h', DoubleType()),
        StructField('low_24h', DoubleType()),
        StructField('price_change_24h', DoubleType()),
        StructField('price_change_percentage_24h', DoubleType()),
        StructField('circulating_supply', DoubleType()),
        StructField('total_supply', DoubleType()),
        StructField('max_supply', DoubleType()),
        StructField('ath', DoubleType()),
        StructField('ath_change_percentage', DoubleType()),
        StructField('ath_date', StringType()),
        StructField('atl', DoubleType()),
        StructField('atl_change_percentage', DoubleType()),
        StructField('atl_date', StringType()),
        StructField('last_updated', StringType())
    ])

    value_df = raw_markets_df.select(
        from_json(col("value")
                  .cast("string"), schema=schema_coingecko_markets_api)
        .alias("value")
    )

    value_df.printSchema()

    data_type_casting_df = value_df.select("value.*") \
        .withColumn("ath_date", to_timestamp(col("ath_date"))) \
        .withColumn("atl_date", to_timestamp(col("atl_date"))) \
        .withColumn("last_updated", to_timestamp(col("last_updated"))) \
        .withColumn("total_volume", col("total_volume").cast("float")) \
        .withColumn("circulating_supply", col("circulating_supply").cast("float")) \

    cleansed_df = data_type_casting_df \
        .withColumn("days_from_ath", datediff("last_updated", "ath_date")) \
        .withColumn("days_from_atl", datediff("last_updated", "atl_date")) \
        .withColumn("circulating_movement",
                    when((col("current_price").isNull()) |
                         (col("current_price") == 0), None)
                    .otherwise((col("total_volume") / col("current_price")) / col("circulating_supply"))*100)

    # Print first 5 rows of cleansed DataFrame
    cleansed_df.show(5, truncate=False)

    write_df = cleansed_df.write \
        .format("mongo") \
        .mode("append") \
        .option("database", mongodb_database) \
        .option("collection", mongodb_collection) \
        .option("uri","mongodb://root:root@mongodb:27017/") \
        .save()
