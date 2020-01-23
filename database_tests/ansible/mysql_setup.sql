ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root123password';
FLUSH PRIVILEGES;
CREATE USER 'ztf'@'localhost' IDENTIFIED BY '123password';
CREATE USER 'ztf'@'%' IDENTIFIED BY '123password';
CREATE DATABASE ztf;
GRANT ALL PRIVILEGES ON ztf.* TO 'ztf'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'ztf'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

