from pyspark import SparkConf
from pyspark.sql import SparkSession, Window
from pyspark.sql.types import *
from pyspark.sql.functions import *
import os
import sys


if __name__ == "__main__":

    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    conf = SparkConf() \
        .setAppName("asm2_spark") \
        .setMaster("spark://spark-master:7077") \
        .set("spark.sql.legacy.timeParserPolicy", "LEGACY") \
        .set("spark.mongodb.write.connection.uri", "mongodb://root:root@mongodb:27017/") \
        .set("spark.mongodb.read.connection.uri", "mongodb://root:root@mongodb:27017/")
        # .set("spark.mongodb.input.uri", "mongodb://127.0.0.1/") \
        # .set("spark.mongodb.output.uri", "mongodb://127.0.0.1/") \

    spark = SparkSession \
        .builder \
        .config(conf=conf) \
        .getOrCreate()
    
    # spark.sql("CREATE DATABASE IF NOT EXISTS ASM2")
    # spark.catalog.setCurrentDatabase("ASM2")

    # spark.sql("DROP TABLE IF EXISTS asm2.ques_tbl")
    # spark.sql("DROP TABLE IF EXISTS asm2.ans_tbl")


    ques_df = spark.read \
        .format("mongo") \
        .option("database", "asm2") \
        .option("collection", "questions") \
        .option("uri","mongodb://root:root@mongodb:27017/") \
        .load()
    
    ques_df.printSchema()
    ques_df.show(2)

    ans_df = spark.read \
        .format("mongo") \
        .option("database", "asm2") \
        .option("collection", "answers") \
        .option("uri","mongodb://root:root@mongodb:27017/") \
        .load()

    ans_df.show(2)
    ans_df.printSchema()


    # spark.sql("CREATE DATABASE IF NOT EXISTS ASM2")
    # spark.catalog.setCurrentDatabase("ASM2")

    # spark.sql("DROP TABLE IF EXISTS asm2.ques_tbl")
    # spark.sql("DROP TABLE IF EXISTS asm2.ans_tbl")


    # ques_df \
    #     .coalesce(1) \
    #     .write \
    #     .mode("overwrite") \
    #     .bucketBy(10, "Id") \
    #     .saveAsTable("ques_tbl")

    # ans_df \
    #     .coalesce(1) \
    #     .write \
    #     .mode("overwrite") \
    #     .bucketBy(10, "ParentId") \
    #     .saveAsTable("ans_tbl")

    question_df = ques_df \
        .withColumnRenamed("Id", "QuestionID")
    
    answer_df = ans_df \
        .withColumnRenamed("Id", "AnswerID")
    
    join_spec = question_df.QuestionID == answer_df.ParentId

    output_df = question_df \
        .join(answer_df, join_spec, "inner") \
        .groupBy("QuestionID") \
        .agg(count("AnswerID").alias("NumberOfAnswer")) \
        .orderBy("QuestionID") \
        .select("QuestionID", "NumberOfAnswer")

    output_df.show(5)

    output_df.repartition(1)

    output_df.coalesce(1) \
        .write \
        .option("header", "true") \
        .option("format", "csv") \
        .option("delimiter", ",") \
        .mode("overwrite") \
        .save("/opt/spark/spark_output/asm2_spark.csv")


    print("completed final task")
    