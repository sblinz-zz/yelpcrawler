##############################################################################################
# The Everything Pin Project
# 
# File: lib\sandbox.py
# Desc: testing space
##############################################################################################

import restaurant_crawler as rc

url = "http://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco&ns=1"
html = rc.GetHTMLStringFromURL(url)
json_str = rc.RegExJSONFromYelpListPage(html)
db_dicts = rc.GetDBDictsFromYelpJSON(rc.json.loads(json_str))

for dict in db_dicts:
	for key in dict:
		print key, dict[key]

"""

def ScrapeAndSaveYelpItems(city, class):
  list_of_items = scrape_yelp(city, class.yelp_type)
  for each item in list_of_items:
    class.new(item).save_to_db

#####################################################

##########################
#Connect to DB
##########################
conn = psycopg2.connect(("dbname='{}' user='{}' host='{}' password='{}' port='{}'").format(private.DB_NAME, private.DB_USERNAME, private.DB_HOST, private.DB_PASSWORD, private.DB_PORT))
cursor = conn.cursor()

private = imp.load_source('', 'private_data.py')
cities = imp.load_source('', 'cities.py')

######################################################################################

def insert_new_restaurant(name=DUMMY_NAME, long=DUMMY_LONG, lat=DUMMY_LAT, address=DUMMY_ADDRESS, rating=DUMMY_RATING, price=DUMMY_PRICE, url=DUMMY_URL):
	cursor.execute("INSERT INTO restaurants (name, longitude, latitude, address, rating, price_range, url) values ('%s', '%d', '%d', '%s', '%d', '%d', '%s')" % (name, long, lat, address, rating, price, url))
	conn.commit()

def read_all_restaurant_names():
	cursor.execute("SELECT name FROM restaurants")
	return cursor.fetchall()

def get_web_page(url):
	data = urllib2.urlopen(url)
	print data.read()

########################################################################
  
insert_new_restaurant("Arby")
insert_new_restaurant("Wendy", 130.121, 122.1121)
print read_all_restaurant_names()
"""