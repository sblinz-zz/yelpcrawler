##############################################################################################
# The Everything Pin Project
# 
# File: lib\sandbox.py
# Desc: testing space
##############################################################################################

import imp
import psycopg2
import urllib2
import json
import re

cc= imp.load_source('', 'city_crawler.py')
private = imp.load_source('', 'private.py')
ylc = imp.load_source('', 'yelp_list_crawler.py')
yi = imp.load_source('', 'yelp_item.py')

##############################################################################################
"""
TEST: Main operations: crawl, push to DB, print items
"""
SF = cc.CityCrawler('San Francisco', 'CA')
SF.Crawl()

conn = psycopg2.connect(("dbname='{}' user='{}' password='{}' host='{}' port='{}'").format( \
							private.DB_NAME, private.DB_USERNAME, private.DB_PASSWORD, private.DB_HOST, private.DB_PORT))

f = open('sandbox.log', 'w')
for crawler in SF.yelp_crawlers:
	crawler.PushItemsToDB(conn)
	f.write("Yelp Category: " + cc.CityCrawler.yelp_cats[SF.yelp_crawlers.index(crawler)] + '\n')
	for item in crawler.items:
		f.write("\tItem #: " + str(crawler.items.index(item)) + '\n')
		for key in item.values:
			if item.values[key] != None:
				f.write("\t" + key + ": " + str(item.values[key]) + '\n')
				if key == 'url' and 'adredir' in item.values[key]:
					f.write(item.values[key] + '\n')
conn.close()

##############################################################################################

"""
TEST: Crawl new 'snippet' url which has a big JSON containing all DB info for all items
Status: Success
Notes: The item data in this URL is upated based on the start parameter so can be used to grab all items.
		Regex match failure is stop condition.

city = "San Francisco"
state = "CA"
city = city.replace(' ', '+')
cat = "Restaurants"
start = 900
grab = True
f = open("sandbox.log", "w")

while True:
	url = "http://www.yelp.com/search/snippet?find_desc=" + cat + "&find_loc=" + city + "%2C+" + state + "&start=" + str(start)
	try:
		data = urllib2.urlopen(url)
		data = data.read()
	except ValueError:
		print "Error: Invalid URL request"

	yelp_list_regex = re.compile(r'"markers":.*?(?P<markers>"[0-9]+".*\}{3,3})')
	if data != None:

		#Check that the regex is grabbing the right sub-JSON
		#yelp_list_json_match = yelp_list_regex.search(data)
		#if yelp_list_json_match != None:
		#	f.write(yelp_list_json_match.group("markers"))
		#	f.write("\n########################################\n")
	
		yelp_list_json_match = yelp_list_regex.search(data)
		if yelp_list_json_match != None:
			json_str = "{" + yelp_list_json_match.group("markers")
			json_dict = json.loads(json_str)
			for key in json_dict:
				try:
					int(key) 		#json main keys (should be) numbers of each item as they appear in the list		
				except ValueError:
					continue

				curr_item = {}
				if 'url' in json_dict[key]:
					curr_item['url'] = json_dict[key]['url']
				if 'location' in json_dict[key]:
					if 'longitude' in json_dict[key]['location']:
						curr_item['longitude'] = json_dict[key]['location']['longitude']
					if 'latitude' in json_dict[key]['location']:
						curr_item['latitude'] = json_dict[key]['location']['latitude']	
				print curr_item
		else:
			print "done at start = " + str(start)
			break;
		start+=10
"""
	