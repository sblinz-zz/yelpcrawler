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

	cats = ["name", "longitude", "latitude", "address", "phone", "rating", "price", "url", "search_phrase"]

	###################
	#Initializers
	###################
	def __init__(self, search_phrase):
		self.values = {}
		
		for col in self.__class__.cats:
			self.values[col] = None
		self.values['search_phrase'] = search_phrase		#yelp search phrase under which this item was listed