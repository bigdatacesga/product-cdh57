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

#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
import os
import sys
import json
import subprocess
from tempfile import mkstemp
from shutil import move
from os import remove, close

reload(sys)  
sys.setdefaultencoding('utf8')

def replace_opts(conf):

	all = conf['nodes']
	master0 = all[0]
	master1 = all[1]
	masters = all[0:2]
	slaves = all[2:]

	nodes_commas = ",".join(map(str, all))
	nodes_lines = "\n".join(map(str, all))
	# Zookeeper se arranca por defecto sólo en los maestros
	nodes_zookeeper = "\n".join("server." + str(masters.index(n)+1) + "=" + n + ":2888:3888" for n in masters)
	nodes_zookeeper_commas = ",".join(map(str, masters))
	nodes_zookeeper_ports = ",".join(n + ":2181" for n in masters)
	disks = conf['disks']
	
	# PARÁMETROS AUTOMÁTICOS
	conf['opts']['hadoop_master_hostname'] = master0
	conf['opts']['hadoop_secondary_hostname'] = master1
	conf['opts']['hadoop_history_hostname'] = master0
	conf['opts']['hadoop_nodes_lines'] = nodes_lines
	conf['opts']['hadoop_jbod_namenode'] = ",".join("file:///data/" + str(n) + "/dfs/nn" for n in range(1,disks['master0'] + 1))
	conf['opts']['hadoop_jbod_datanode'] = ",".join("file:///data/" + str(n) + "/dfs/dn" for n in range(1,disks['slaves'] + 1))
	conf['opts']['hadoop_jbod_yarn_local'] = ",".join("file:///data/" + str(n) + "/yarn/local" for n in range(1,disks['slaves'] + 1))
	conf['opts']['hadoop_jbod_yarn_logs'] = ",".join("file:///data/" + str(n) + "/yarn/logs" for n in range(1,disks['slaves'] + 1))
	
	# ZOOKEEPER
	conf['opts']['zookeeper_master_hostname'] = master0
	conf['opts']['zookeeper_nodes_ports_commas'] = nodes_zookeeper_ports
	conf['opts']['zookeeper_nodes_commas'] = nodes_zookeeper_commas
	conf['opts']['zookeeper_nodes_cfg'] = nodes_zookeeper
	conf['opts']['zookeeper_data'] = "/data/1/zookeeper" # Esta variable debería venir en la plantilla
	
	# HBASE
	conf['opts']['hbase_master_hostname'] = master0
	conf['opts']['hbase_nodes_lines'] = nodes_lines
	
	# HIVE
	conf['opts']['hive_master_hostname'] = master0
	
	# OOZIE
	conf['opts']['oozie_master_hostname'] = master0
	
	# SPARK
	conf['opts']['spark_master_hostname'] = master0
	conf['opts']['spark_nodes_lines'] = nodes_lines
	
	# SQOOP
	conf['opts']['sqoop_master_hostname'] = master0
	
	# POSTGRESQL
	conf['opts']['postgresql_master_hostname'] = master0
	
	# IMPALA
	conf['opts']['impala_master_hostname'] = master0
	
	# SOLR
	conf['opts']['solr_master_hostname'] = master0
	
	opts = {}
	for option in conf['opts']:
		opts[option.replace("_", ".")] = conf['opts'][option]
	
	modify_files(opts)
	
	
def replace(path, variable, value):
    fh, tmp = mkstemp()
    with open(tmp,'w') as new_file:
        with open(path) as old_file:
            for line in old_file:
                new_file.write(line.replace(variable, value))
    close(fh)
    remove(path)
    move(tmp, path)
	
	
def modify_files(opts):

	# Carpetas locales que contienen los archivos de configuración
	folders = """flume hadoop hadoop-httpfs hbase hbase-solr hive hive-hcatalog 
	hive-webhcat hue impala mahout oozie pig solr spark sqoop2 zookeeper"""
	
	# Obtención de los directorios completos
	folders = " ".join("/etc/" + n + "/conf.current" for n in map(str, folders.split()))
	dirs = folders.split()

	# Obtención de los archivos de configuración
	files = []
	for dir in dirs:
		bashcmd = "find " + dir + " -type f"
		process = subprocess.Popen(bashcmd.split(), stdout=subprocess.PIPE)
		files += process.communicate()[0].split()

	for file in files:
		for opt in opts:
			replace(file, "{{" + opt + "}}", opts[opt])
		os.chmod(file, 0644)
			

if __name__ == '__main__':
	replace_opts(json.loads(sys.argv[1]))
