FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get -y install curl

# JAVA
#ARG JAVA_ARCHIVE=http://download.oracle.com/otn-pub/java/jdk/8u102-b14/server-jre-8u102-linux-x64.tar.gz
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:webupd8team/java -y
RUN apt-get update -y


RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y oracle-java8-installer
RUN apt-get install -y build-essential manpages-dev python3-dev libblas-dev \
    liblapack-dev libatlas-base-dev
#RUN apt-get install -y python-numpy python-scipy python-matplotlib ipython \
#ipython-notebook python-pandas
#RUN ln -s /usr/bin/python3 /usr/bin/python
ENV PATH $PATH:/usr/bin/python
#ENV JAVA_HOME /usr/bin/java
#ENV PATH $PATH:$JAVA_HOME/bin
#RUN curl -s --insecure \
#--header "Cookie: oraclelicense=accept-securebackup-cookie;" ${JAVA_ARCHIVE} \
#| tar -xz -C /usr/local/ && ln -s $JAVA_HOME /usr/local/java 

# SPARK
ARG SPARK_ARCHIVE=http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz
ENV SPARK_HOME /usr/local/spark-2.0.2-bin-hadoop2.7

ENV PATH $PATH:${SPARK_HOME}/bin
RUN curl -s ${SPARK_ARCHIVE} | tar -xz -C /usr/local/

ADD . /home/nate/docker/spark_2.0
WORKDIR /home/nate/docker/spark_2.0
RUN apt-get install -y python-pip
RUN pip install -r requirements.txt
#RUN pip3 install --upgrade setuptools 
#RUN pip3 install numpy scipy ipython[all] jupyter pandas \
#    sympy nose enum wcwidth

WORKDIR $SPARK_HOME
