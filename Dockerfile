FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get -y install curl
RUN apt -y install vim

# JAVA
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:webupd8team/java -y
RUN apt-get update -y


RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y oracle-java8-installer
RUN apt-get update -y
RUN apt-get install -y build-essential manpages-dev python3-dev libblas-dev \
    liblapack-dev libatlas-base-dev vim

# SPARK
ARG SPARK_ARCHIVE=http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz
ENV SPARK_HOME /usr/local/spark-2.0.2-bin-hadoop2.7
ENV PATH $PATH:${SPARK_HOME}/bin
RUN curl -s ${SPARK_ARCHIVE} | tar -xz -C /usr/local/

#JDBC Drivers for connecting to postgres db
ADD https://jdbc.postgresql.org/download/postgresql-9.4.1212.jre6.jar \
    ${SPARK_HOME}/jars

#Python path and libraries
ENV PATH $PATH:/usr/bin/python
ENV PYTHONPATH=/usr/local/lib/python2.7/dist-packages:${SPARK_HOME}/python/pyspark:\
${SPARK_HOME}/python/lib/py4j-0.10.3-src.zip:${SPARK_HOME}/python/lib/pyspark.zip
ADD . /home/nate/docker/spark_2.0
WORKDIR /home/nate/docker/spark_2.0
RUN apt-get install -y python-pip
RUN pip install -r requirements.txt
ENV PYSPARK_DRIVER_PYTHON=/usr/local/bin/ipython

ENV SPARK_MASTER_PORT 7077
ENV SPARK_MASTER_WEBUI_PORT 8080
ENV SPARK_WORKER_PORT 8888
ENV SPARK_WORKER_WEBUI_PORT 8081

EXPOSE 8080 7077 8888 8081 4040 7001 7002 7003 7004 7005 7006

WORKDIR $SPARK_HOME
