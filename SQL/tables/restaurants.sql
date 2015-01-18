-- Restaurant Table

CREATE TABLE RESTAURANTS
(
id serial primary key, --auto-incrementing primary key for each row
name varchar(255),
longitude decimal(11,8),
latitude decimal(11,8),
address varchar(255), --street address
rating decimal(2,1), --yelp rating
price_range smallint, --number of yelp dollar signs
url varchar(255)
);