#!/bin/bash

# For each user who will be submitting MapReduce jobs using MapReduce v2 (YARN), or running Pig, Hive, or Sqoop
export HADOOP_MAPRED_HOME=/usr/lib/hadoop-mapreduce

# For Livy
export SPARK_HOME=/usr/lib/spark
export HADOOP_CONF_DIR=/etc/hadoop/conf

