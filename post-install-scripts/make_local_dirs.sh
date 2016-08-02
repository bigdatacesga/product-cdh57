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

for i in $(eval echo {1..$1});
do
	# Directorios y permisos para DataNode / NameNode
	mkdir -p /data/$i/dfs/dn /data/$i/dfs/nn
	chmod -R 700 /data/$i/dfs
	chown -R hdfs:hdfs /data/$i/dfs
	
	# Directorios y permisos de directorios locales de ZooKeeper
	mkdir -m 700 /data/$i/zookeeper && chown zookeeper:zookeeper /data/$i/zookeeper
	
	# Directorios y permisos de directorios locales de YARN
	# local-dirs
	mkdir -p /data/$i/yarn/local; \
	# log-dirs
	mkdir /data/$i/yarn/logs; \
	# Permissions
	chmod -R 755 /data/$i/yarn; \
	chown -R yarn:yarn /data/$i/yarn
done
