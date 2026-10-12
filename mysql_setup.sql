-- One-time setup of the local MySQL used by the database examples.
-- Run it as the MySQL administrator, e.g.:  mysql -u root -p < mysql_setup.sql
-- The user/password match the defaults in db_config.py (lab use only!).

CREATE DATABASE IF NOT EXISTS EmbeddedLab;
CREATE USER IF NOT EXISTS 'labuser'@'localhost' IDENTIFIED BY 'labpass';
GRANT ALL PRIVILEGES ON EmbeddedLab.* TO 'labuser'@'localhost';
FLUSH PRIVILEGES;
