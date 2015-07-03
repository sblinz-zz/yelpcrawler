##############################################################################################
# Yelp Crawler
# 
# File: city_crawler.py
# Desc: wrapper class for crawling an entire city
##############################################################################################

import db
import yelp_list_crawler as ylc

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

	def crawl_yelp(self):
		for ylc in self.yelp_crawlers:		
			ylc.crawl(self.yelp_db, 0, 9)
		self.yelp_db.close()