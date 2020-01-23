# The now() function is a built-in MySQL function that returns the current date and time.
SELECT now()

# Oracle provides a table called dual, which consists of a single column called dummy that contains a single row of data.
SELECT now() FROM dual;

SHOW databases;

CREATE DATABASE <DB Name>

USE <DB Name>



CREATE TABLE person
(person_id SMALLINT UNSIGNED,
fname VARCHAR(20),
lname VARCHAR(20),
gender ENUM('M','F'),
birth_date DATE,
street VARCHAR(30),
city VARCHAR(20),
state VARCHAR(20),
country VARCHAR(20),
postal_code VARCHAR(20),
CONSTRAINT pk_person PRIMARY KEY (person_id)
);


CREATE TABLE favorite_food
(person_id SMALLINT UNSIGNED,
food VARCHAR(20),
CONSTRAINT pk_favorite_food PRIMARY KEY (person_id, food), CONSTRAINT fk_fav_food_person_id FOREIGN KEY (person_id)
REFERENCES person (person_id));



SELECT
a.person_id,a.fname , b.food
FROM person a INNER JOIN favorite_food b ON a.person_id=b.person_id;

ALTER TABLE person MODIFY person_id SMALLINT UNSIGNED AUTO_INCREMENT;
