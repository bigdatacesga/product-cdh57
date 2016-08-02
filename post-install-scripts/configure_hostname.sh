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

# Configuración del host
hostname $(hostname); if cat /etc/sysconfig/network | grep -q HOSTNAME=; \
then sed -i "s/HOSTNAME=.*/HOSTNAME=$(hostname)/g" /etc/sysconfig/network; \
else echo "HOSTNAME="$(hostname) >> /etc/sysconfig/network; fi; \
if ! cat /etc/hosts | grep -q "\s$(hostname)$"; \
then echo -e $(hostname -I | awk '{print $1}')"\t"$(hostname) >> /etc/hosts; fi
