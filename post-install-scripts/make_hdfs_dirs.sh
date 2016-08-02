#
#    Post install scripts for product-cdh57 
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

#!/bin/bash

# Formatear HDFS
su - hdfs -c "hdfs namenode -format"

service hadoop-hdfs-datanode start
service hadoop-hdfs-namenode start

su - hdfs -c "hdfs dfsadmin -safemode leave"

# Directorios y permisos de directorios en HDFS
# /tmp directory
su - hdfs -c "hdfs dfs -mkdir /tmp"
su - hdfs -c "hdfs dfs -chmod -R 1777 /tmp"
# Staging directory
su - hdfs -c "hdfs dfs -mkdir /user"
su - hdfs -c "hdfs dfs -chmod 755 /user"
# History directory
su - hdfs -c "hdfs dfs -mkdir /user/history"
su - hdfs -c "hdfs dfs -chmod -R 1777 /user/history"
su - hdfs -c "hdfs dfs -chown mapred:hadoop /user/history"
# Logs de YARN en HDFS
su - hdfs -c "hdfs dfs -mkdir -p /var/log/hadoop-yarn"
su - hdfs -c "hdfs dfs -chmod -R 1777 /var/log/hadoop-yarn"
su - hdfs -c "hdfs dfs -chown yarn:mapred /var/log/hadoop-yarn"
# Directorios para los usuarios de MRv2
su - hdfs -c "hdfs dfs -mkdir /user/root"
su - hdfs -c "hdfs dfs -chown root:root /user/root"
# Directorio para HBase
su - hdfs -c "hdfs dfs -mkdir /hbase"
su - hdfs -c "hdfs dfs -chown hbase:hbase /hbase"
# Directorios para Hive
su - hdfs -c "hdfs dfs -mkdir -p /hive/warehouse"
su - hdfs -c "hdfs dfs -chmod -R 1777 /hive/warehouse"
su - hdfs -c "hdfs dfs -chown -R hive:hive /hive"
# Directorios para Oozie
su - hdfs -c "hdfs dfs -mkdir -p /user/oozie"
su - hdfs -c "hdfs dfs -chmod -R 1777 /user/oozie"
su - hdfs -c "hdfs dfs -chown oozie:oozie /user/oozie"
# Directorios para Spark
su - hdfs -c "hdfs dfs -mkdir /user/spark"
su - hdfs -c "hdfs dfs -mkdir /user/spark/applicationHistory "
su - hdfs -c "hdfs dfs -chown -R spark:spark /user/spark"
su - hdfs -c "hdfs dfs -chmod 1777 /user/spark/applicationHistory"
# Directorios para Hue
su - hdfs -c "hdfs dfs -mkdir /user/hue"
su - hdfs -c "hdfs dfs -chown -R hue:hue /user/hue"

service hadoop-hdfs-datanode stop
service hadoop-hdfs-namenode stop

