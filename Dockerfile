# VERSION 2.2.3
# AUTHOR: Steven Brandt (@ednarb29)
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t ednarb29/docker-airflow .
# SOURCE: https://github.com/ednarb29/docker-airflow
# BASED ON: https://github.com/puckel/docker-airflow (Matthieu "Puckel_" Roisil)

FROM python:3.9-slim-buster
LABEL maintainer="ednarb29"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=2.2.3
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS="spark,mongo,docker"
ARG PYTHON_DEPS="wtforms==2.3.3"
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ARG SPARK_VERSION=3.0.2
ARG HADOOP_VERSION=3.2
ENV AIRFLOW_GPL_UNIDECODE yes

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

USER root

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip install --upgrade pip \
    && pip install --upgrade pyparsing \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install celery==5.2.7 \
    && pip install flower==2.0.1 \
    && pip install apache-airflow[crypto,postgres,hive,jdbc,mysql,ssh,redis${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base


# Install OpenSSH client
RUN apt-get update && \
    apt-get install -y openssh-client && \
    apt-get clean;


RUN pip uninstall markupsafe -y
RUN pip install markupsafe==2.0.1
RUN apt-get update && apt-get install libpq5 -y
RUN pip install mysql-connector-python
RUN pip uninstall httpcore -y
RUN pip uninstall httpx -y
RUN pip install httpcore==0.15.0
RUN pip install httpx==0.23.0
RUN pip install configparser
RUN pip install mysqlclient==2.1.1



RUN pip uninstall pyopenssl -y
RUN pip uninstall cryptography -y
RUN pip uninstall Twisted -y

RUN pip install autopep8==1.6.0 
RUN pip install beautifulsoup4==4.11.1 
RUN pip install kafka-python==2.0.2 
RUN pip install requests==2.28.1 
RUN pip install requests-file==1.5.1 
RUN pip install Scrapy==2.6.2 
RUN pip install scrapy-selenium==0.0.7 
RUN pip install scrapy-splash==0.9.0 
RUN pip install selenium==4.11.2 
RUN pip install Unidecode==1.2.0 
RUN pip install urllib3==1.26.11 
RUN pip install webdriver-manager==4.0.0 
RUN pip install websocket-client==0.58.0 
RUN pip install whatthepatch==1.0.2 
RUN pip install XlsxWriter==3.0.3 
RUN pip install xlwings==0.27.15 
RUN pip install yapf==0.31.0 
RUN pip install zict==2.1.0 
RUN pip install zipp==3.8.0 
RUN pip install cookiecutter==1.7.3 
RUN pip install pandas 
RUN pip install lxml==4.6.4 
RUN pip install pyopenssl==22.0.0 
RUN pip install cryptography==37.0.0 
RUN pip install Twisted==22.10.0
RUN pip install confluent-kafka

ENV SPARK_HOME /usr/local/spark

# Spark submit binaries and jars (Spark binaries must be the same version of spark cluster)
# Download and uncompress spark from the apache archive
RUN curl --fail --location --output apache-spark.tgz "https://archive.apache.org/dist/spark/spark-3.0.2/spark-3.0.2-bin-hadoop3.2.tgz" \
&& mkdir -p /usr/local/spark \
&& tar -xf apache-spark.tgz -C /usr/local/spark --strip-components=1 \
&& rm apache-spark.tgz


# Download required driver for working between Airflow and MongoDB
RUN curl --no-verbose -O --output /usr/local/spark/jars/mongo-java-driver-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.12.2/mongo-java-driver-3.12.2.jar"
RUN curl --no-verbose -O --output /usr/local/spark/jars/mongodb-driver-core-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/3.12.2/mongodb-driver-core-3.12.2.jar"
RUN curl --no-verbose -O --output /usr/local/spark/jars/mongodb-driver-sync-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/3.12.2/mongodb-driver-sync-3.12.2.jar"
RUN curl --no-verbose -O --output /usr/local/spark/jars/bson-3.12.2.jar "https://repo1.maven.org/maven2/org/mongodb/bson/3.12.2/bson-3.12.2.jar"


# Create SPARK_HOME env var
RUN export SPARK_HOME
ENV PATH $PATH:/usr/local/spark/bin


COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
