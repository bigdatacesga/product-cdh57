#
#    Dockerfile for product-cdh57 
#    Copyright (C) 2016 Rodrigo Martínez <dev@brunneis.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
    
#################################################################
# CDH 5.7 (Not installed: KMS, Sentry, Sqoop 1, Whirr)
#################################################################

FROM brunneis/centos-jdk8:7.1
MAINTAINER "Rodrigo Martínez" <dev@brunneis.com>

# UPDATE & DEPENDENCIES
RUN yum -y update && yum clean all

ENV REFRESHED_AT 2016-04-18

# MAIN CDH REPO
RUN wget http://archive.cloudera.com/cdh5/redhat/7/x86_64/cdh/cloudera-cdh5.repo \
-O /etc/yum.repos.d/cloudera-cdh5.repo; \

# EXTRAS CDH REPO
wget http://archive.cloudera.com/gplextras5/redhat/7/x86_64/gplextras/cloudera-gplextras5.repo \
-O /etc/yum.repos.d/cloudera-gplextras5.repo; \

# CLOUDERA GPG KEY
rpm --import http://archive.cloudera.com/cdh5/redhat/7/x86_64/cdh/RPM-GPG-KEY-cloudera; \

yum -y install \
#################################################################
# CDH COMPONENTS INSTALLATION                                    
#################################################################
# RESOURCE MANAGER
hadoop-yarn-resourcemanager \

# NAMENODE
hadoop-hdfs-namenode \

# SECONDARY NAMENODE
hadoop-hdfs-secondarynamenode \

# NODEMANAGER, DATANODE, MAPREDUCE
hadoop-yarn-nodemanager hadoop-hdfs-datanode hadoop-mapreduce \

# HISTORY SERVER, PROXY SERVER
hadoop-mapreduce-historyserver hadoop-yarn-proxyserver \

# HADOOP CLIENT
hadoop-client \

# LZO COMPRESSION
hadoop-lzo \

# CRUNCH
crunch \

# FLUME
flume-ng flume-ng-agent \

# HBASE
hbase hbase-master hbase-regionserver hbase-thrift hbase-rest \

# HIVE / HCATALOG
hive hive-metastore hive-server2 hive-hcatalog hive-webhcat hive-webhcat-server hive-hbase \

# HTTPFS
hadoop-httpfs \

# HUE
hue hue-search cyrus-sasl-gssapi cyrus-sasl-plain libxml2 libxslt zlib python sqlite python-psycopg2 \

# IMPALA
impala impala-server impala-state-store impala-catalog impala-shell \

# MAHOUT
mahout \

# OOZIE
oozie oozie-client \

# PIG
pig pig-udf-datafu  \

# CLOUDERA SEARCH (SOLR BASED)
solr-server solr-crunch solr-mapreduce hbase-solr-indexer \

# SPARK
spark-core spark-master spark-worker spark-history-server spark-python \

# SQOOP 2
sqoop2-server sqoop2-client \

# ZOOKEEPER
zookeeper zookeeper-server \

#################################################################
# OTHER PACKAGES                        
#################################################################
# POSTGRESQL
postgresql-server postgresql-jdbc \

# NTP
ntp \

# BIND-UTILS (dig)
bind-utils \

#################################################################
# FOR DEVELOPMENT                     
#################################################################
nano net-tools

#################################################################
# BASE CONFIGURATION FILES
#################################################################
ADD conf/base_conf.tar.gz /etc/


RUN \

# HADOOP
alternatives --install /etc/hadoop/conf hadoop-conf /etc/hadoop/conf.current 50; \
alternatives --set hadoop-conf /etc/hadoop/conf.current; \

# ZOOKEEPER
alternatives --install /etc/zookeeper/conf zookeeper-conf /etc/zookeeper/conf.current 50; \
alternatives --set zookeeper-conf /etc/zookeeper/conf.current; \

# FLUME
alternatives --install /etc/flume-ng/conf flume-conf /etc/flume-ng/conf.current 50; \
alternatives --set flume-conf /etc/flume-ng/conf.current; \

# HBASE
alternatives --install /etc/hbase/conf hbase-conf /etc/hbase/conf.current 50; \
alternatives --set hbase-conf /etc/hbase/conf.current; \

# HIVE / HCATALOG
alternatives --install /etc/hive/conf hive-conf /etc/hive/conf.current 50; \
alternatives --set hive-conf /etc/hive/conf.current; \
alternatives --install /etc/hive-hcatalog/conf hcatalog-conf /etc/hive-hcatalog/conf.current 50; \
alternatives --set hcatalog-conf /etc/hive-hcatalog/conf.current; \
ln -s /usr/share/java/postgresql-jdbc.jar /usr/lib/hive/lib/postgresql-jdbc.jar; \

# MAHOUT
alternatives --install /etc/mahout/conf mahout-conf /etc/mahout/conf.current 50; \
alternatives --set mahout-conf /etc/mahout/conf.current; \

# OOZIE
alternatives --install /etc/oozie/conf oozie-conf /etc/oozie/conf.current 50; \
alternatives --set oozie-conf /etc/oozie/conf.current; \
alternatives --install /etc/oozie/tomcat-conf oozie-tomcat-conf /etc/oozie/tomcat-conf.http 50; \
alternatives --set oozie-tomcat-conf /etc/oozie/tomcat-conf.http; \

# PIG
alternatives --install /etc/pig/conf pig-conf /etc/pig/conf.current 50; \
alternatives --set pig-conf /etc/pig/conf.current; \

# SPARK
alternatives --install /etc/spark/conf spark-conf /etc/spark/conf.current 50; \
alternatives --set spark-conf /etc/spark/conf.current; \

# SQOOP 2
alternatives --install /etc/sqoop2/conf sqoop2-conf /etc/sqoop2/conf.current 50; \
alternatives --set sqoop2-conf /etc/sqoop2/conf.current; \
alternatives --install /etc/sqoop2/tomcat-conf sqoop2-tomcat-conf /etc/sqoop2/tomcat-conf.http 50; \
alternatives --set sqoop2-tomcat-conf /etc/sqoop2/tomcat-conf.http; \
ln -s /usr/share/java/postgresql-jdbc.jar /var/lib/sqoop2/; \

# HADOOP-HTTPFS
alternatives --install /etc/hadoop-httpfs/conf hadoop-httpfs-conf /etc/hadoop-httpfs/conf.current 50; \
alternatives --set hadoop-httpfs-conf /etc/hadoop-httpfs/conf.current; \
alternatives --install /etc/hadoop-httpfs/tomcat-conf hadoop-httpfs-tomcat-conf /etc/hadoop-httpfs/tomcat-conf.http 50; \
alternatives --set hadoop-httpfs-tomcat-conf /etc/hadoop-httpfs/tomcat-conf.http; \

# HBASE-SOLR
alternatives --install /etc/hbase-solr/conf hbase-solr-conf /etc/hbase-solr/conf.current 50; \
alternatives --set hbase-solr-conf /etc/hbase-solr/conf.current; \

# HIVE-WEBHCAT
alternatives --install /etc/hive-webhcat/conf hive-webhcat-conf /etc/hive-webhcat/conf.current 50; \
alternatives --set hive-webhcat-conf /etc/hive-webhcat/conf.current; \

# HUE
alternatives --install /etc/hue/conf hue-conf /etc/hue/conf.current 50; \
alternatives --set hue-conf /etc/hue/conf.current; \

# IMPALA (EMPTY)
alternatives --install /etc/impala/conf impala-conf /etc/impala/conf.current 50; \
alternatives --set impala-conf /etc/impala/conf.current; \

# SOLR
alternatives --install /etc/solr/conf solr-conf /etc/solr/conf.current 50; \
alternatives --set solr-conf /etc/solr/conf.current; \
alternatives --install /etc/solr/tomcat-conf solr-tomcat-conf /etc/solr/tomcat-conf.http 50; \
alternatives --set solr-tomcat-conf /etc/solr/tomcat-conf.http


#################################################################
# OTHER FILES                              
#################################################################
ADD conf/scripts.tar.gz /
COPY conf/cdh.sh /etc/profile.d/cdh.sh
COPY conf/sshpass /usr/bin/
RUN chmod u+x /usr/bin/sshpass /*.sh

#################################################################
# DISABLE THE CDH SERVICES ON BOOT                          
#################################################################
RUN systemctl disable \
	flume-ng-agent.service \
	hadoop-hdfs-datanode.service \
	hadoop-hdfs-namenode.service \
	hadoop-hdfs-secondarynamenode.service \
	hadoop-httpfs.service \
	hadoop-mapreduce-historyserver.service \
	hadoop-yarn-nodemanager.service \
	hadoop-yarn-proxyserver.service \
	hadoop-yarn-resourcemanager.service \
	hbase-master.service \
	hbase-regionserver.service \
	hbase-solr-indexer.service \
	hive-metastore.service \
	hive-server2.service \
	hive-webhcat-server.service \
	impala-catalog.service \
	impala-server.service \
	impala-state-store.service \
	network.service \
	oozie.service \
	solr-server.service \
	spark-history-server.service \
	spark-master.service \
	spark-worker.service \
	zookeeper-server.service \
	sqoop2-server.service \
	hue.service \
	postgresql.service


#################################################################
# PASSWORD ROOT FOR ROOT USER                          
#################################################################
RUN echo "root" | passwd --stdin root; \
sed -ri 's/^PasswordAuthentication\sno/PasswordAuthentication yes/' /etc/ssh/sshd_config; \
sed -ri 's/^PermitRootLogin\swithout-password/PermitRootLogin yes/' /etc/ssh/sshd_config

CMD ["/usr/sbin/init"]
