##############################################################################################
# The Everything Pin Project
# 
# File: lib\sandbox.py
# Desc: testing space
##############################################################################################

import imp

cc= imp.load_source('', 'city_crawler.py')
SF = cc.CityCrawler('San Francisco', 'CA')
SF.Crawl()

for crawler in SF.yelp_crawlers:
	print "Yelp Category: " + cc.CityCrawler.yelp_cats[SF.yelp_crawlers.index(crawler)]
	for item in crawler.items:
		print "\tItem #: " + str(crawler.items.index(item))
		for key in item.details:
			if item.details[key] != None:
				print "\t" + key + ": " + str(item.details[key])

"""
##########################
#Connect to DB
##########################

import psycopg2 				#PostgreSQL connectivity

conn = psycopg2.connect(("dbname='{}' user='{}' host='{}' password='{}' port='{}'").format(private.DB_NAME, private.DB_USERNAME, private.DB_HOST, private.DB_PASSWORD, private.DB_PORT))
cursor = conn.cursor()

######################################################################################

def insert_new_restaurant(name=DUMMY_NAME, long=DUMMY_LONG, lat=DUMMY_LAT, address=DUMMY_ADDRESS, rating=DUMMY_RATING, price=DUMMY_PRICE, url=DUMMY_URL):
	cursor.execute("INSERT INTO restaurants (name, longitude, latitude, address, rating, price_range, url) values ('%s', '%d', '%d', '%s', '%d', '%d', '%s')" % (name, long, lat, address, rating, price, url))
	conn.commit()

def read_all_restaurant_names():
	cursor.execute("SELECT name FROM restaurants")
	return cursor.fetchall()

def get_web_page(url):
	data = urllib2.urlopen(url)
	print data.read()

########################################################################
  
insert_new_restaurant("Arby")
insert_new_restaurant("Wendy", 130.121, 122.1121)
print read_all_restaurant_names()
"""