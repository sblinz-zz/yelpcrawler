##############################################################################################
# The Everything Pin Project
# 
# File: lib\sandbox.py
# Desc: testing space
##############################################################################################

import imp

cc= imp.load_source('', 'city_crawler.py')

##############################################################################################
"""
TEST: Main operations: crawl, push to DB, print items

TO DO:
	1. Catch and parse 'search_results' attribute from snippet JSON
	2. Implement duplicate checking before pushing to DB
	3. Implement logging functionality
	4. Correct YelpCityCrawler.Crawl() while loop wrt start/stop params
"""
SF = cc.CityCrawler('San Francisco', 'CA')
SF.CrawlYelp()

##############################################################################################
	