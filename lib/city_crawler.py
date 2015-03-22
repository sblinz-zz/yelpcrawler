##############################################################################################
# The Everything Pin Project
# 
# File: lib\city_crawler.py
# Desc: wrapper class for crawling an entire city
##############################################################################################

import imp 						#better module importing

#load local modules
db = imp.load_source('', 'db.py')
ylc = imp.load_source('', 'yelp_list_crawler.py')

class CityCrawler:

	#####################
	#Class Variables
	#####################
	yelp_search_phrases = ["Restaurants"]	#yelp search_phrases to crawl
	
	def __init__(self, city, state, yelp_search_phrases=yelp_search_phrases):
		self.city = city
		self.state = state
		self.yelp_crawlers = [ylc.YelpListCrawler(self.city, self.state, search_phrase) for search_phrase in yelp_search_phrases]
		self.yelp_db = db.YelpDBConn()

	def CrawlYelp(self):
		for ylc in self.yelp_crawlers:
			ylc.Crawl(self.yelp_db, 0, 10)