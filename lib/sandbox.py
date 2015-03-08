##############################################################################################
# The Everything Pin Project
# 
# File: lib\sandbox.py
# Desc: testing space
##############################################################################################

import imp

cc= imp.load_source('', 'city_crawler.py')
ylc = imp.load_source('', 'yelp_list_crawler.py')
yi = imp.load_source('', 'yelp_item.py')

##############################################################################################
"""
TEST: Main operations: crawl, push to DB, print items
"""
SF = cc.CityCrawler('San Francisco', 'CA')
SF.Crawl()

##############################################################################################
	