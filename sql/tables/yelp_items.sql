-- Table of Yelp Items

CREATE TABLE YELP_ITEMS
(
id serial primary key, 			--auto-incrementing primary key for each row
name varchar(255),
longitude decimal(11,8),
latitude decimal(11,8),
address varchar(255), 			--street address
rating decimal(2,1), 			--yelp rating
price smallint, 				--number of yelp dollar signs
url varchar(255)
cat varchar(255)				--yelp category
);