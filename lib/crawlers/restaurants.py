##############################################################################################
# The Everything Pin Project
# 
# File: restaurants.py
# Desc: crawler and parser for restaurant data
#
##############################################################################################

#local modules
from private_data import * #DB connectivity info, etc.

#libraries
import psycopg2 #PostgreSQL library
import urllib2 #URL capture

##########################
#Connect to PostgreSQL DB
##########################
conn = psycopg2.connect(("dbname='{0}' user='{1}' host='{2}' password='{3}' port='{4}'").format(DB_NAME, DB_USERNAME, DB_HOST, DB_PASSWORD, DB_PORT))
cursor = conn.cursor()

##########################
#Basic methods
##########################
def insert_new_restaurant(name):
	cursor.execute("insert into restaurants (name) values ('%s')" % (name))
	conn.commit()

def read_all_restaurant_names():
	cursor.execute("SELECT name FROM restaurants")
	return cursor.fetchall()

def get_web_page(url):
	data = urllib2.urlopen(url)
	print data.read()
  
insert_new_restaurant("test")
print read_all_restaurant_names()