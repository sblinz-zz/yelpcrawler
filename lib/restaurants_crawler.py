##############################################################################################
# The Everything Pin Project
# 
# File: lib\restaurant_crawler.py
# Desc: crawler and parser for restaurant data
##############################################################################################

#system
import imp #for better module importing

#packages
import psycopg2 #PostgreSQL connectivity
import urllib2 #URL capture
from bs4 import BeautifulSoup
import re

#load local modules
private = imp.load_source('', 'private_data.py')
cities = imp.load_source('', 'cities.py')
rests = imp.load_source('', 'restaurant.py')

##########################
#Connect to DB
##########################
conn = psycopg2.connect(("dbname='{}' user='{}' host='{}' password='{}' port='{}'").format(private.DB_NAME, private.DB_USERNAME, private.DB_HOST, private.DB_PASSWORD, private.DB_PORT))
cursor = conn.cursor()

#################################################################################
# YELP LIST PAGE PARSER - Parses DB data from any Yelp page with a list of items
#
#	-Each such page has a JSON at the bottom of the page containing a tail URL,
#		longitude/latitude for each of the items on the page
#	-regex capture the smallest JSON containing this data
#	-JSON parse into objects for each Yelp item
#	-URL tail appears in HTML anchor of items text and img link
#	-HTML parse the list page and rest of DB data from HTML surrounding URL tail
#
#################################################################################

def GetURL(url):
	data = urllib2.urlopen(url)
	return data

#######################################
#RegEx Test: use static Yelp list page
#######################################
SF_restaurants_pg1 = GetURL("http://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA&ns=1")

yelp_list_regex = re.compile(r'Controller.*(?P<yelp_list_json>\{"1.*\}{3,3})')
yelp_list_json = yelp_list_regex.search(SF_restaurants_pg1.read())
if yelp_list_json != None:
	print yelp_list_json.group('yelp_list_json)


