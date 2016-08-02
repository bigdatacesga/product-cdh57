#
#    Fabfile for product-cdh57 
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

#!/usr/bin/env python
# encoding: utf-8
"""Orquestration template

The following tasks must be implemented:
    - start
    - stop
    - restart
    - status

An instance endpoint has to be provided using the INSTANCE environment variable.
For example:

    INSTANCE="instances/user/cdh/5.7.0/1"

A fabric roledef  is created for each service defined in the registry.
It can be used with the decorator: @roles('servicename1')

WARN: The hosts are accesed using the IP address of the first network device,
usually eth0.

The properties of a given service can be accessed through:

    SERVICES['servicename'].propertyname

for example:

    SERVICES['namenode'].heap

Details about a given node can be obtained through each Node object returned by service.nodes

The fabfile can be tested running it in NOOP mode (testing mode) exporting a NOOP env variable.
"""
from __future__ import print_function
import os
import sys
import json
from fabric.api import *
from fabric.colors import red, green, yellow
from fabric.contrib.files import exists
# FIXME: Installing configuration-registry with pip and importing registry directly does not work
#  inside the fabfile. Temporarily it is copied manually in the utils directory
import registry
# from utils import registry

if os.environ.get('INSTANCE'):
    INSTANCE = os.environ.get('INSTANCE')
else:
    eprint(red('An instance endpoint has to be provided using the INSTANCE environment variable'))
    sys.exit(2)

if os.environ.get('REGISTRY'):
    REGISTRY = os.environ.get('REGISTRY')
else:
    REGISTRY = 'http://registry'

# Retrieve info from the registry
registry.connect(REGISTRY)
cluster = registry.Cluster(INSTANCE)
nodes = cluster.nodes
services = cluster.services

# Expose the relevant information
NODES = [node.name for node in nodes]
SERVICES = [service.name for service in services]

env.user = 'root'
env.password = 'root'

# GET HOSTNAMES FROM IPs
env.hosts = [n.networks[1].address for n in nodes]
for service in services:
    env.roledefs[service.name] = [n.networks[1].address for n in service.nodes]
    
all = env.hosts[0:]
master0 = [env.hosts[0]]
master1 = [env.hosts[1]]
slaves = env.hosts[2:]

#
# Debugging mode
#
# To enable it use: export NOOP=1
if os.environ.get('NOOP'):

    print(yellow('\n\n== Running in NOOP mode ==\n\n'))

    def run(name):
        print('[{0}] run: {1}'.format(env.host, name))

    def put(source, destination):
        print('[{0}] put: {1} {2}'.format(env.host, source, destination))

    @task
    @parallel
    def hostname():
        """Print the hostnames: mainly used for testing purposes"""
        run('/bin/hostname')

@task
@runs_once
def start():

	##########################################
	# Main configuration
	##########################################
	
	# Configuración de hostname
	execute(configure_hostname) # CNF
	
	# Substitution of the variables
	execute(replace_opts) # CNF
	
	# All the data of previous installations is deleted
	execute(clean_jbod) # CNF
	
	# Making local needed directories in each node
	execute(make_local_dirs) # CNF
	
	# Setting the user limits configuration
	execute(set_user_limits) # CNF
	
	# Copy pubkey from the hadoop master to its slaves
	execute(copy_hadoop_pubkey) # CNF
	
	# Copye pubkey from the spark master to its slaves
	execute(copy_spark_pubkey) # CNF

	##########################################
	# Start services
	##########################################
	
	execute(start_hadoop_hdfs_dn) # SRV
	
	# Make HDFS needed directories
	execute(make_hdfs_dirs) # CNF
	
	execute(start_hadoop_hdfs_nn) # SRV
	execute(start_hadoop_hdfs_snn) # SRV

	execute(start_hadoop_yarn_nm) # SRV
	execute(start_hadoop_yarn_rm) # SRV
	execute(start_hadoop_mapreduce_hs) # SRV

	execute(start_spark_master) # SRV
	execute(start_spark_hs) # SRV
	execute(start_spark_worker) # SRV
	

#############################################
# MAIN CONFIGURATION
#############################################
@task
@parallel
def configure_hostname():
	run('/configure_hostname.sh')

@task
@parallel
def replace_opts(): 
	conf = {
		"nodes": all,
		"disks": {
			"master0": len(nodes[NODES.index("master0")].disks),
			"master1": len(nodes[NODES.index("master1")].disks),
			"slaves": len(nodes[NODES.index("slave0")].disks)
		},
		"opts": {
			"hadoop_hdfs_blocksize": services[SERVICES.index("hadoop-hdfs-datanode")].hadoop_hdfs_blocksize,
			"hadoop_mapreduce_map_memory": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_mapreduce_map_memory,
			"hadoop_mapreduce_map_heap": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_mapreduce_map_heap,
			"hadoop_mapreduce_map_cores": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_mapreduce_map_cores,
			"hadoop_mapreduce_reduce_memory": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_mapreduce_reduce_memory,
			"hadoop_mapreduce_reduce_heap": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_mapreduce_reduce_heap,
			"hadoop_mapreduce_reduce_cores": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_mapreduce_reduce_cores,
			"hadoop_yarn_nodemanager_memory": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_yarn_nodemanager_memory,
			"hadoop_yarn_containers": services[SERVICES.index("hadoop-yarn-nodemanager")].hadoop_yarn_containers,
			}
	}
	
	run('python /replace_opts.py \'' + json.dumps(conf) + '\'')

@task
@parallel
def clean_jbod():
	run('/clean_jbod.sh ' + str(len(nodes[all.index(env.host_string)].disks)))
	
@task
@parallel
def make_local_dirs():
	run('/make_local_dirs.sh ' + str(len(nodes[all.index(env.host_string)].disks)))

@task
@parallel
def set_user_limits():
	run('/set_user_limits.sh')

@task
@roles('hadoop-yarn-resourcemanager')	
def copy_hadoop_pubkey():
	# Los argumentos del script son los esclavos correspondientes y el master
	run('/copy_pubkey.sh ' + env.host_string + ' ' + ' '.join(slaves))

@task
@roles('spark-master')
def copy_spark_pubkey():
	# Los argumentos del script son los esclavos correspondientes y el master
	run('/copy_pubkey.sh ' + env.host_string + ' ' + ' '.join(slaves))

@task
@roles('hadoop-hdfs-namenode')
def make_hdfs_dirs():
	run('/make_hdfs_dirs.sh')


#############################################
# START SERVICES
#############################################
@task
@roles('hadoop-hdfs-namenode')
def start_hadoop_hdfs_nn():
	run('service hadoop-hdfs-namenode start')

@task
@parallel
@roles('hadoop-hdfs-datanode')
def start_hadoop_hdfs_dn():
	run('service hadoop-hdfs-datanode start')

@task
@roles('hadoop-hdfs-secondarynamenode')
def start_hadoop_hdfs_snn():
	run('service hadoop-hdfs-secondarynamenode start')


@task
@parallel
@roles('hadoop-yarn-nodemanager')
def start_hadoop_yarn_nm():
	run('service hadoop-yarn-nodemanager start')

@task
@roles('hadoop-yarn-resourcemanager')
def start_hadoop_yarn_rm():
	run('service hadoop-yarn-resourcemanager start')

@task
@roles('hadoop-mapreduce-historyserver')
def start_hadoop_mapreduce_hs():
	run('service hadoop-mapreduce-historyserver start')


@task
@roles('spark-master')
def start_spark_master():
	run('service spark-master start')

@task
@roles('spark-history-server')
def start_spark_hs():
	run('service spark-history-server start')

@task
@parallel
@roles('spark-worker')
def start_spark_worker():
	run('service spark-worker start')


#############################################
# STOP SERVICES
#############################################
@task
@roles('hadoop-hdfs-namenode')
def stop_hadoop_nn():
	run('service hadoop-hdfs-namenode stop')

@task
@parallel
@roles('hadoop-hdfs-datanode')
def stop_hadoop_dn():
	run('service hadoop-hdfs-datanode stop')

@task
@roles('hadoop-hdfs-secondarynamenode')
def stop_hadoop_snn():
	run('service hadoop-hdfs-secondarynamenode stop')


@task
@parallel
@roles('hadoop-yarn-nodemanager')
def stop_hadoop_yarn_nm():
	run('service hadoop-yarn-nodemanager stop')

@task
@roles('hadoop-yarn-resourcemanager')
def stop_hadoop_yarn_rm():
	run('service hadoop-yarn-resourcemanager stop')

@task
@roles('hadoop-mapreduce-historyserver')
def stop_hadoop_mapreduce_hs():
	run('service hadoop-mapreduce-historyserver stop')


@task
@roles('spark-master')
def stop_spark_master():
	run('service spark-master stop')

@task
@roles('spark-history-server')
def stop_spark_hs():
	run('service spark-history-server stop')

@task
@parallel
@roles('spark-worker')
def stop_spark_worker():
	run('service spark-worker stop')


