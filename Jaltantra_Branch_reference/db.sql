CREATE DATABASE IF NOT EXISTS jaltantra_db;
CREATE USER 'jaltantra_branch'@'localhost' IDENTIFIED BY 'jaltantra_branch';
GRANT ALL PRIVILEGES ON jaltantra_db.* TO 'jaltantra_branch'@'localhost';
FLUSH PRIVILEGES;

USE jaltantra_db;
CREATE TABLE IF NOT EXISTS jaltantra_users (
    id              INT                         NOT NULL    AUTO_INCREMENT PRIMARY KEY,
    fullname        VARCHAR(100)    DEFAULT     NULL,
    username        VARCHAR(100)                NOT NULL,
    organization    VARCHAR(150)    DEFAULT     NULL,
    state           VARCHAR(100)    DEFAULT     NULL,
    country         VARCHAR(50)     DEFAULT     NULL,
    email           VARCHAR(150)    DEFAULT     NULL,
    password        VARCHAR(255)    DEFAULT     NULL,
    creationDate    DATETIME        DEFAULT                 CURRENT_TIMESTAMP
);
