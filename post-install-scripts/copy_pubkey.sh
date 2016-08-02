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

#/bin/bash

# Generar claves y añadir como autorizada la propia clave pública
echo -e 'y\n' | ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
ssh-keyscan 0.0.0.0 >> ~/.ssh/known_hosts
ssh-keyscan localhost >> ~/.ssh/known_hosts
ssh-keyscan $(hostname) >> ~/.ssh/known_hosts

# Copiar la clave pública a todos los esclavos
for slave in $@; do
	sshpass -p root ssh-copy-id $slave -o StrictHostKeyChecking=no
done

# Deshabilitar acceso ssh con contraseña
# sed -ri 's/^PasswordAuthentication\syes/PasswordAuthentication no/' /etc/ssh/sshd_config
# sed -ri 's/^PermitRootLogin\syes/PermitRootLogin without-password/' /etc/ssh/sshd_config
# service sshd restart
