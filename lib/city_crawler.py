##############################################################################################
# The Everything Pin Project
# 
# File: lib\city_crawler.py
# Desc: wrapper class for crawling an entire city
##############################################################################################

import imp 						#better module importing

#load local modules
private = imp.load_source('', 'private.py')
ylc = imp.load_source('', 'yelp_list_crawler.py')

class CityCrawler:

	#####################
	#Class Variables
	#####################
	yelp_search_phrases = ["Restaurants"]	#yelp search_phrases to crawl
	
	def __init__(self, city, state, yelp_search_phrases=yelp_search_phrases):
		self.conn = None 	#psycopg2 DB connection object
		self.city = city
		self.state = state
		self.yelp_crawlers = [ylc.YelpListCrawler(self.city, self.state, search_phrase) for search_phrase in yelp_search_phrases]

	def ConnectToDB(self):
		self.conn = psycopg2.connect(("dbname='{}' user='{}' password='{}' host='{}' port='{}'").format( \
							private.DB_NAME, private.DB_USERNAME, private.DB_PASSWORD, private.DB_HOST, private.DB_PORT))

	def CrawlYelp(self):
		for ylc in self.yelp_crawlers:
			ylc.Crawl(self.conn, 0, 200)

	def Crawl(self):
		self.ConnectToDB()
		self.CrawlYelp()
		self.conn.close()
		