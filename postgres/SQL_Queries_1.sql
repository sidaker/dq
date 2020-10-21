
-- https://github.com/ami-levin/Animal_Shelter/blob/master/01%20-%20Create%20database%20and%20reference%20data.sql

select * from customers
where last_name IS DISTINCT FROM 'Smith';

select * from customers
where (last_name = 'Smith') IS NOT TRUE;

CREATE SCHEMA Reference;

CREATE TABLE Reference.Common_Person_Names
(
	rank	SMALLINT		NOT NULL PRIMARY KEY,
	Surname VARCHAR(20) NOT NULL UNIQUE,
	Male	VARCHAR(20) NOT NULL UNIQUE,
	Female	VARCHAR(20) NOT NULL UNIQUE
);


INSERT INTO Reference.Species (Species)
VALUES ('Dog'), ('Cat'), ('Rabbit'),
('Ferret'), ('Raccoon');-- And a couple species for which we won't have any animals
