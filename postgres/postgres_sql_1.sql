SELECT version();
-- "PostgreSQL 12.4 on x86_64-apple-darwin16.7.0, compiled by Apple LLVM version 8.1.0 (clang-802.0.42), 64-bit"
SELECT now();
-- "2020-10-20 11:26:24.900017+01"

CREATE DATABASE colors (ColorID int, ColorName char(20));

INSERT INTO colors VALUES (1, 'red'), (2, 'blue'), (3, 'green');

SELECT * FROM colors;

ALTER TABLE db.TABLE
  ALTER COLUMN "c1" TYPE charcter(30) COLLATE "en_US";

ALTER TABLE table_name
  ADD COLUMN new_column_name data_type constraint;

ALTER TABLE customers
  ALTER COLUMN contact_name SET NOT NULL;

ALTER TABLE users
  ALTER COLUMN name SET DATA TYPE character varying(255) COLLATE "en_US";
-- native Postgres data types.
-- integer
-- character(n)
