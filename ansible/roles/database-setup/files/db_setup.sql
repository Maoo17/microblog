CREATE USER 'exporter' @'localhost' IDENTIFIED BY 'password' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS,
REPLICATION CLIENT,
SELECT
  ON *.* TO 'exporter' @'localhost';