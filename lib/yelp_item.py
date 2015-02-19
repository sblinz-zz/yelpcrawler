##############################################################################################
# The Everything Pin Project
# 
# File: lib\yelp_item.py
# Desc: Base class representing a generic yelp item
##############################################################################################

##########################################
#Basic class 
##########################################
class YelpItem:

	#corresponds to columns in 'yelp_item' DB
	categories = ["name", "longitude", "latitude", "address", "rating", "price", "url", "cat"]

	###################
	#Initializers
	###################
	def __init__(self, cat):
		self.details = {}
		for col in self.__class__.categories:
			self.details[col] = None
		self.details['cat'] = cat 	#high-level yelp category searched which gave this item