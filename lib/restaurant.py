##############################################################################################
# The Everything Pin Project
# 
# File: lib\restaurants.py
# Desc: "Restaurants & Bars" category data structures
##############################################################################################

##########################################
#Control variables
#see sql\tables\restaurants.sql for cols
##########################################
DUMMY_PKEY = -1
DUMMY_NAME = ""
DUMMY_LONG = 181
DUMMY_LAT = 91
DUMMY_ADDRESS = ""
DUMMY_RATING = -1
DUMMY_PRICE = 0
DUMMY_URL = ""

MIN_PKEY = 0
MIN_LONG = -180
MIN_LAT = -90
MIN_RATING = 0
MIN_PRICE = 1

MAX_LONG = 180
MAX_LAT = 90
MAX_RATING = 5
MAX_PRICE = 4

MAX_RESTAURANT_RADIUS = 10 #miles

##########################################
#Basic class 
##########################################
class Restaurant:
	#constructors
	def __init__(self):
		self._pkey = DUMMY_PKEY
		self._name = DUMMY_NAME
		self._longitude = DUMMY_LONG
		self._latitude = DUMMY_LAT
		self._address = DUMMY_ADDRESS
		self._rating = DUMMY_RATING
		self._price = DUMMY_PRICE
		self._url = DUMMY_URL
		
	def __init__(name, long, lat, address, rating, price, url, pkey=DUMMY_PKEY):
		self._pkey = DUMMY_PKEY
		self._name = name
		self._longitude = long
		self._latitude = lat
		self._address = address
		self._rating = rating
		self._price = price
		self._url = url
		
		
	####################################
	#DB methods
	####################################
	
	#static fetch methods
	
	#ConstructWithinThreshByLongLat()
	#Desc: Construct instances for each item at ever increasing radii of (long, lat) until threshold number is found (or hit MAX_RADIUS)
	#Return: an array of Restaurant objects
	@staticmethod
	def ConstructWithinThreshByLongLat(long, lat, thresh):
		print
	
	#ConstructWithinRadiusByLongLat()
	#Desc: Construct instances for each restaurant within a given radius of (long, lat)
	#Return: an array of Restaurant objects	
	@staticmethod
	def ConstructWithinRadiusByLongLat(long, lat, radius):
		print

	#ConstructFromDB()
	#Desc: Construct instances of restaurants matching non-dummy parameters
	#Return: an array of Restaurant objects
	@staticmethod
	def ConstructFromDB(cursor, name=DUMMY_NAME, long=DUMMY_LONG, lat=DUMMY_LAT, address=DUMMY_ADDRESS, rating=DUMMY_RATING, price=DUMMY_PRICE, url=DUMMY_URL,pkey=DUMMY_PKEY):
		print
	
	#push methods
	
	#Push()
	#Desc: insert an entry corresponding to this instance in the DB
	#Return: bool (success/failure)
	def Push(cursor):
		print
	
	