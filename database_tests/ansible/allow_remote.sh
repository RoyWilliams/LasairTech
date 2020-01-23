cd /etc/mysql/mysql.conf.d
sed 's/bind-address/#bind-address/' mysqld.cnf > junk; mv junk mysqld.cnf
service mysql restart

