# builder step used to download and configure spark environment
FROM openjdk:11.0.11-jre-slim-buster as builder

# Set JAVA_HOME
# ENV JAVA_HOME /usr/local/openjdk-11

# Add Dependencies for PySpark and SSH
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy openssh-client

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1


# Fix the value of PYTHONHASHSEED
# Note: this is needed when you use Python 3.3 or greater
ENV SPARK_VERSION=3.0.2 \
HADOOP_VERSION=3.2 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1 \
JAVA_HOME=/usr/local/openjdk-11

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz

# Download MongoDB Spark Connector JAR
RUN wget --no-verbose -O /opt/spark/jars/mongo-spark-connector_2.12-3.0.2.jar "https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.2/mongo-spark-connector_2.12-3.0.2.jar"

# Download MongoDB Java Driver Core JAR
RUN wget --no-verbose -O /opt/spark/jars/mongo-java-driver-4.4.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.9.1/mongo-java-driver-3.9.1.jar"

# Add the MongoDB Java driver JAR to the classpath
RUN wget --no-verbose -O /opt/spark/jars/mongodb-driver-sync-4.2.3.jar "https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/4.2.3/mongodb-driver-sync-4.2.3.jar" 
RUN wget --no-verbose -O /opt/spark/jars/mongo-java-driver-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.2/mongo-java-driver-3.12.2.jar"
RUN wget --no-verbose -O /opt/spark/jars/mongodb-driver-core-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/3.12.2/mongodb-driver-core-3.12.2.jar"
RUN wget --no-verbose -O /opt/spark/jars/mongodb-driver-sync-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/3.12.2/mongodb-driver-sync-3.12.2.jar"
RUN wget --no-verbose -O /opt/spark/jars/bson-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/bson/3.12.2/bson-3.12.2.jar"

# Apache spark environment
FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=9999 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=9999 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 9999 7077 6066

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG
RUN pip3 install pyspark

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]
