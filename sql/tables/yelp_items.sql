-- Table of Yelp Items

CREATE TABLE YELP_ITEMS
(
id serial primary key, 					--auto-incrementing primary key for each row
name varchar(255),
longitude decimal(16,13),
latitude decimal(16,13),
address varchar(255), 					--street address
rating decimal(2,1), 					--yelp rating
price smallint, 						--number of yelp dollar signs
phone varchar(255),						--phone number as a string
url varchar(255),
search_phrase varchar(255)				--search phrase under which this item was listed
);