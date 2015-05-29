##############################################################################################
# The Everything Pin Project
# 
# File: lib\yelp_list_crawler.py
# Desc: crawler class for any yelp list page; creates an array of YelpItem objects
##############################################################################################

#packages
import imp 				#nice module importing
import urllib2 			#URL capture
import re 				#regex's
import json				#parsing json string <-> python dictionary
import psycopg2			#DB connection

#load local modules
yi = imp.load_source('', 'yelp_item.py')

#####################################################################################
# YELP LIST PAGE CRAWLER - Grab DB data from Yelp 'snippet' pages
#	
#	GRABBING BASIC DB INFO:
#	-A so-called 'snippet' URL can be built for a given category, location, and 
#		item start number which returns one large JSON.
#			
#	http://www.yelp.com/search/snippet?find_desc=Restaurants&find_loc=San%20Francisco%2C%20CA&start=10
#
#	-This JSON contains an attribute 'markers' which holds basic DB data we care
#		about on the 10 items from start+1 to start+10: url, longitude, latitude:
#
#		"markers" : 
#		{
#			...
#			"105" : 
#				{ 
#				...
#				"url" : "biz/la-ciudad-de-mexico-san-francisco",
#		 		"location" :
#					{ "latitude" : 37.784610600000001, "longitude" : -122.46443840000001 }
#				}
#				...
#			...
#		}
#
#	-regex capture the markers JSON
#	-parse the markers json into YelpItem instances for each of the items
#
#	GRABBING REMAINING DB INFO:
#	-Each item attribute in the 'markers' JSON has an attribute 'search_results' 
#		whose value is a string that contains the url and the remaining DB info we
#		care about for all 10 items.
#
######################################################################################

class YelpListCrawler:

	def __init__(self, city, state, search_phrase):
		self.city = city.replace(' ', '%20')
		self.state = state
		self.search_phrase = search_phrase			#passed to each YelpItem
		self.items = []								#array of YelpItem objects
		self.snippet_url = "http://www.yelp.com/search/snippet?find_desc=" + \
							str(self.search_phrase) + "&find_loc=" + str(self.city) +  \
							"%2C+" + str(self.state) + "&start=" 

	def get_url_data(self, url):
		"""
		@url is identifier for logging
		"""
		try:
			data = urllib2.urlopen(url)
			data_str = data.read()
			if data_str != None:
				return data_str
			else:
				print "[Err] URL data empty - " + url
				return None
		except ValueError:									#Incorrect URL format
			print "[Err] Invalid URL format - " + url
		except urllib2.URLError:							#Cannot connect to URL
			print "[Err] Could not connect to URL - " + url 

		return None

	def get_markers_json_from_snippet_data(self, snippet_data, ident='No ID'):
		"""
		Regex capture the 'markers' JSON string from the full snippet data

		Params:
			@snippet_data: a string of the full snippet data
			@ident: logging identification
		"""
		if snippet_data != None:
			snippet_markers_json_regex = re.compile(r'"markers":.*?(?P<markers>"[0-9]+".*\}{3,3})')
			snippet_markers_regex_match = snippet_markers_json_regex.search(snippet_data)
			if snippet_markers_regex_match != None:
				return "{" + snippet_markers_regex_match.group('markers')
			else:
				print "[Err] No match for 'markers' JSON in snippet data - " + ident

		return None

	def get_data_from_markers_json(self, markers_json, ident='No ID'):
		"""
		Snippet JSON attribute 'markers' contains attributes url, longitude, latitude
		Create YelpItem instances and fill these details

		Params:
			@markers_json: a string of the markers json
			@ident: logging identification

		Modify:
			Add newly created YelpItems to member array self.items
		"""
		try:
			json_dict = json.loads(markers_json)
		except ValueError:
			print "[Err] Converting 'markers' JSON failed - " + ident
			return

		for item_no in json_dict:
			try:
				int(item_no) 		#json main item_nos (should be) numbers of each item as they appear in the list		
			except ValueError:
				continue

			curr_item = YelpItem(self.search_phrase)

			#capture items URL attribute
			if 'url' in json_dict[item_no]:
				curr_item.values['url'] = json_dict[item_no]['url']
			else:
				print "[Err] URL attribute missing from 'markers' JSON item - " + str(item_no) + " : " + ident

			#capture items location attribute
			if 'location' in json_dict[item_no]:
				if 'longitude' in json_dict[item_no]['location']:
					curr_item.values['longitude'] = json_dict[item_no]['location']['longitude']
				else:
					print "[Err] Location : longitude attribute missing from 'markers' JSON item - " + str(item_no) + " : " + ident

				if 'latitude' in json_dict[item_no]['location']:
					curr_item.values['latitude'] = json_dict[item_no]['location']['latitude']	
				else:
					print "[Err] Location : latitude attribute missing from 'markers' JSON item - " + str(item_no) + " : " + ident

			else:
				print "[Err] Location attribute missing from 'markers' JSON item - " + str(item_no) + " : " + ident

			self.items.append(curr_item)

	def crawl(self, db, start=0, end=None, push_period=100):
		"""
		Crawl Yelp list page(s) for this instances city, state, and search_phrase 

		Params:
			@start: the first snippet url start number to crawl
			@end: the last snippet url start number to crawl (inclusive)
			@push_period: how often to push the populated YelpItems to the DB and flush; must be a multiple of 10
		"""
		item_count = start
		snippet_data = None
		markers_json = None

		url_fail_count = None
		json_fail_count = None

		#push_period must be a multiple of 10, the number of items per snippet page
		if push_period % 10 != 0:
			push_period = 100

		while item_count <= end:
			if len(self.items) == push_period:
				try:
					self.push_items_to_db(db)
					self.flush()
				except psycopg2.DataError as e:
					print "[Err] Data error pushing row to DB - " + e.pgerror.replace('ERROR: ', '')
			
			ident = 'start=' + str(item_count)
			
			if url_fail_count == 4:
				print "[Err] 4 URL errors...stopping crawl - " + ident

			if json_fail_count == 4:
				print "[Err] 4 'markers' JSON errors...stopping crawl - " + ident
			
			url = self.snippet_url + str(item_count)
			snippet_data = self.get_url_data(url)
			if snippet_data != None:
				markers_json = self.get_markers_json_from_snippet_data(snippet_data, ident)
			else:
				url_fail_count += 1
				continue				#don't count failed json extraction if URL failed

			if markers_json != None:
				self.get_data_from_markers_json(markers_json, ident)
			else:
				json_fail_count += 1

			item_count += 10

	def push_items_to_db(self, db):
		print "[Msg] Pushing " + str(len(self.items)) + " items to DB"
		cats = YelpItem.cats
		c = db.conn.cursor()

		for item in self.items:
			SQL = "INSERT INTO " + db.table + " ("
			for i in range(len(cats)):
				if i != len(cats)-1:
					SQL += cats[i] + ","
				else:
					SQL += cats[i] + ") VALUES ("

			for i in range(len(cats)):
				if i != len(cats)-1:
					SQL += "%(" + cats[i] + ")s, "
				else:
					SQL += "%(" + cats[i] + ")s);"

			c.execute(SQL, item.values)
			db.conn.commit()

	def flush(self):
		"""
		Empty all YelpItem data captured
		"""
		print "[Msg] Flushing " + str(len(self.items)) + " local item's data"
		self.items = []
		

	