##############################################################################################
# The Everything Pin Project
# 
# File: lib\sandbox.py
# Desc: testing space
##############################################################################################

import imp
import psycopg2

cc= imp.load_source('', 'city_crawler.py')
private = imp.load_source('', 'private.py')
ylc = imp.load_source('', 'yelp_list_crawler.py')
yi = imp.load_source('', 'yelp_item.py')

SF = cc.CityCrawler('San Francisco', 'CA')
SF.Crawl()

"""
TEST: Crawl first 10 entires from static HTML page
Status: Success
"""
"""
for crawler in SF.yelp_crawlers:
	print "Yelp Category: " + cc.CityCrawler.yelp_cats[SF.yelp_crawlers.index(crawler)]
	for item in crawler.items:
		print "\tItem #: " + str(crawler.items.index(item))
		for key in item.details:
			if item.details[key] != None:
				print "\t" + key + ": " + str(item.details[key])
"""

"""
TEST: Push stored yelp items to DB
Status: Success
"""

conn = psycopg2.connect(("dbname='{}' user='{}' password='{}' host='{}' port='{}'").format( \
							private.DB_NAME, private.DB_USERNAME, private.DB_PASSWORD, private.DB_HOST, private.DB_PORT))

for crawler in SF.yelp_crawlers:
	crawler.PushItemsToDB(conn)
conn.close()