CREATE SCHEMA XX
  authorization user1

CREATE SCHEMA human_resources
  authorization postgres;

CREATE TABLE manufacturing.categories
(
    category_id integer NOT NULL,
    name character varying(50) NOT NULL,
    market character varying(20) NOT NULL,
    PRIMARY KEY (category_id)
)

TABLESPACE pg_default;

ALTER TABLE manufacturing.categories
  OWNER to postgres;


ALTER TABLE manufacturing.products
  ADD FOREIGN KEY (category_id)
  REFERENCES manufacturing.categories (category_id) MATCH SIMPLE
  ON UPDATE CASCADE
  ON DELETE NO ACTION;


  CREATE TABLE human_resources.departments
  (
      department_id integer NOT NULL,
      department_name character varying(50) NOT NULL,
      building character varying(50) NOT NULL,
      PRIMARY KEY (department_id)
  )

  TABLESPACE pg_default;

  ALTER TABLE human_resources.departments
      OWNER to postgres;

      CREATE TABLE human_resources.employees
      (
          employee_id integer NOT NULL,
          first_name character varying(50) NOT NULL,
          last_name character varying(50) NOT NULL,
          hire_date date NOT NULL,
          department_id integer NOT NULL,
          PRIMARY KEY (employee_id),
          FOREIGN KEY (department_id)
              REFERENCES human_resources.departments (department_id) MATCH SIMPLE
              ON UPDATE NO ACTION
              ON DELETE NO ACTION
      )

      TABLESPACE pg_default;

      ALTER TABLE human_resources.employees
          OWNER to postgres;

-- JOIN
          -- Create a query that joins related tables together
          SELECT products.product_id,
          	products.product_name AS products_name,
          	products.manufacturing_cost,
          	categories.name AS category_name,
          	categories.market
          FROM manufacturing.products JOIN manufacturing.categories
          	ON products.category_id = categories.category_id
          WHERE market = 'industrial';


          CREATE VIEW manufacturing.product_details AS
          SELECT products.product_id,
          	products.product_name AS products_name,
          	products.manufacturing_cost,
          	categories.name AS category_name,
          	categories.market
          FROM manufacturing.products JOIN manufacturing.categories
          	ON products.category_id = categories.category_id
          WHERE market = 'industrial';
