cd /etc/mysql/mysql.conf.d

# allow remote connections for archive
sed 's/bind-address/#bind-address/' mysqld.cnf > junk; mv junk mysqld.cnf

# allow file writing for nodes
sed 's%secure-file-priv.*%secure-file-priv="/var/lib/mysql-files"%' mysqld.cnf > junk; mv junk mysqld.cnf

service mysql restart



