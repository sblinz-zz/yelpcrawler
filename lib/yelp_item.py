##############################################################################################
# The Everything Pin Project
# 
# File: lib\yelp_item.py
# Desc: class representing a generic yelp item
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
		self.values = {}
		for col in self.__class__.categories:
			self.values[col] = None
		self.values['cat'] = cat 	#high-level yelp category searched which gave this item