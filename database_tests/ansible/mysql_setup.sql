SET GLOBAL validate_password_length = 6;
SET GLOBAL validate_password_special_char_count = 0;
SET GLOBAL validate_password_mixed_case_count = 0;
SET GLOBAL validate_password_policy = 'LOW';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'EH107HWpostcode';
FLUSH PRIVILEGES;
CREATE USER 'ztf'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'ztf'@'%' IDENTIFIED BY 'password';
CREATE DATABASE ztf;
GRANT ALL PRIVILEGES ON ztf.* TO 'ztf'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'ztf'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

