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

	#####################
	#Class Variables
	#####################

	yelp_cat = ["Restuarants", "Bars"]	#yelp categories that are crawled
	
	def __init__(city, state):
		self.city = city
		self.state = state
		self.yelp_crawlers = [ylc.YelpListCrawler(self.city, self.state, cat) for cat in yelp_types]


	def CrawlYelp():


	def CrawlCity():
		CrawlYelp()
		