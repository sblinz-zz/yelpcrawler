##############################################################################################
# The Everything Pin Project
# 
# File: lib\city_crawler.py
# Desc: wrapper class for crawling an entire city
##############################################################################################

import imp 						#better module importing
import psycopg2 				#PostgreSQL connectivity

#load local modules
ylc = imp.load_source('', 'yelp_list_crawler.py')

class CityCrawler:

	#################
	#Class Variables
	#################
	
	#Yelp specific
	yelp_crawlers = [ylc.YelpListCrawler('Restaurants'), ylc.YelpListCrawler("Bars")]

	def __init__(city):
		self.city = city

	def CrawlYelp():


	def CrawlCity:
		