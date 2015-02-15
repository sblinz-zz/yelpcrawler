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

	#corresponds to DB columns in 'yelp_item' DB
	categories = ["name", "longitude", "latitude", "address", "rating", "price", "url", "yelp_type"]

	###################
	#Initializers
	###################
	def __init__(self, type):
		self.details = {}
		for col in categories:
			self.details[col] = None
		self.details['type'] = type
		
	def __init__(self, values):
		self.details = {}
		for col in categories
			if(values.has_key(col)):
				self.details[col] = values[col]
			else:
				self.detials[col] = None	

	###################
	#DB methods
	###################
	"""
	#static fetch methods
	
	#ConstructWithinThreshBylongitudelatitude()
	#Summary: Construct instances for each item at ever increasing radii of (longitude, latitude) until threshold number is found (or hit MAX_RADIUS)
	#Return: an array of Restaurant objects
	@staticmethod
	def ConstructWithinThreshBylongitudelatitude(longitude, latitude, thresh):
		print
	
	#ConstructWithinRadiusBylongitudelatitude()
	#Summary: Construct instances for each restaurant within a given radius of (longitude, latitude)
	#Return: an array of Restaurant objects	
	@staticmethod
	def ConstructWithinRadiusBylongitudelatitude(longitude, latitude, radius):
		print

	#ConstructFromDB()
	#Summary: Construct instances of restaurants matching non-dummy parameters
	#Return: an array of Restaurant objects
	@staticmethod
	def ConstructFromDB(cursor, name=DUMMY_NAME, longitude=DUMMY_longitude, latitude=DUMMY_latitude, address=DUMMY_ADDRESS, rating=DUMMY_RATING, price=DUMMY_PRICE, url=DUMMY_URL, id=DUMMY_id):
		print
	
	#push methods
	
	#Push()
	#Desc: insert an entry corresponding to this instance in the DB
	#Return: bool (success/failure)
	def Push(cursor):
		print
	"""
	