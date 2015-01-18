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

#load local modules
private = imp.load_source('', 'private_data.py')
cities = imp.load_source('', 'cities.py')
rests = imp.load_source('', 'restaurants.py')

##########################
#Connect to DB
##########################
conn = psycopg2.connect(("dbname='{}' user='{}' host='{}' password='{}' port='{}'").format(private.DB_NAME, private.DB_USERNAME, private.DB_HOST, private.DB_PASSWORD, private.DB_PORT))
cursor = conn.cursor()