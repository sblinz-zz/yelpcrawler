##############################################################################################
# The Everything Pin Project
# 
# File: lib\yelp_list_crawler.py
# Desc: crawler class for any yelp list page; creates an array of YelpItem objects
##############################################################################################

#packages
import imp 						#nice module importing
import urllib2 					#URL capture
import re 						#regex's
import json						#parsing json string <-> python dictionary
import psycopg2					#DB connection
from bs4 import BeautifulSoup 	#html parser

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
#		whose value is a string with html that contains the remaining DB data we need
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
		self.snippet = None			#snippet data for extracting markers json and search_results attribute
		self.markers_json = None	
		self.search_results_html = None

	def get_snippet(self, url):
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

	def get_markers_json_from_snippet(self, snippet, ident='No ID'):
		"""
		Regex capture the 'markers' JSON string from the full snippet data

		Params:
			@snippet: a string of the full snippet data
			@ident: logging identification
		"""
		if snippet != None:
			snippet_markers_json_regex = re.compile(r'"markers":.*?(?P<markers>"[0-9]+".*\}{3,3})')
			snippet_markers_json_regex_match = snippet_markers_json_regex.search(snippet)
			if snippet_markers_json_regex_match != None:
				return "{" + snippet_markers_json_regex_match.group('markers')
			else:
				print "[Err] No match for 'markers' JSON in snippet data - " + ident
				return None

	def get_search_results_html_from_snippet(self, snippet, ident="No ID"):
		"""
		Snippet JSON attribute 'search_results' contains html with remaining DB data

		Params:
			@snippet: a string of the full snippet data
			@ident: logging identification
		"""
		if snippet != None:
			snippet_search_results_html_regex = re.compile(r'"search_results":.*?",')
			snippet_search_results_html_regex_match = snippet_search_results_html_regex.search(snippet)
			if snippet_search_results_html_regex_match != None:
				return 

	def get_list_item_data(self, markers_json, search_results, ident="No ID"):
		"""
		Snippet 'markers' attribute is a JSON with url and location data for each item
		Snippet 'search_results' attribute is HTML with remaining data for each item

		Params:
			@markers_json: string of the markers JSON
			@search_results: string of the search_results HTML
			@ident: logging id

		Modify:
			Add filled YelpItem instance to self.items for each item in markers JSON
		"""

		#create markers dictionary to iterate over this lists items
		try:
			markers_dict = json.loads(markers_json)
		except ValueError:
			print "[Err] Converting 'markers' JSON failed - " + ident
			return

		#iterate over item numbers in markers json
		#skip marker attributes not identifying an item
		for item_no in markers_dict:
			try:
				int(item_no)	
			except ValueError:
				continue

			curr_item = YelpItem(self.search_phrase)
			self.get_item_data_from_markers_dict(curr_item, markers_dict[item_no], ident)
			self.get_item_data_from_search_results_html(curr_item, search_results, ident)
			self.items.append(curr_item)

	def get_item_data_from_markers_dict(self, yelp_item, markers_item_dict, ident='No ID'):
		"""
		Each markers item attribute contains attributes url, longitude, latitude

		Params:
			@yelp_item: YelpItem instance to fill
			@markers_item_dict: a dictionary of the given item in the markers json
			@ident: logging id

		Modify:
			Fill url and location data for given YelpItem instance
		"""

		#capture items URL attribute
		if 'url' in markers_item_dict:
			yelp_item.values['url'] = markers_item_dict['url']
		else:
			print "[Err] URL attribute missing from 'markers' JSON item - : " + ident + " : " + str(item_no) 

		#capture items location attribute
		if 'location' in markers_item_dict:
			if 'longitude' in markers_item_dict['location']:
				yelp_item.values['longitude'] = markers_item_dict['location']['longitude']
			else:
				print "[Err] Location : longitude attribute missing from 'markers' JSON item - " + ident + " : " + str(item_no) 

			if 'latitude' in markers_item_dict['location']:
				yelp_item.values['latitude'] = markers_item_dict['location']['latitude']	
			else:
				print "[Err] Location : latitude attribute missing from 'markers' JSON item - " + ident + " : " + str(item_no)

		else:
			print "[Err] Location attribute missing from 'markers' JSON item - " + ident + " : " + str(item_no)

	def get_item_data_from_search_results_html(self, yelp_item, search_results, ident="No ID"):
		"""
		search_results html contains remaining data to grab, anchored by item url

		Params:
			@yelp_item: YelpItem instance to fill
			@search_results: a string of the search_results html
			@ident: logging identification

		Modify:
			Add newly created YelpItems to member array self.items
		"""
		pass

	def crawl(self, db, start=0, end=None, push_period=100):
		"""
		Crawl Yelp list page(s) for this instances city, state, and search_phrase 

		Params:
			@db: YelpDBConn instance with cursor to Yelp items table
			@start: the first snippet url start number to crawl
			@end: the last snippet url start number to crawl (inclusive)
			@push_period: how often to push the populated YelpItems to the DB and flush; must be a multiple of 10
		"""
		item_count = start

		url_fail_count = 0
		data_fail_count = 0

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

			if data_fail_count == 4:
				print "[Err] 4 insufficient data errors...stopping crawl - " + ident
			
			url = self.snippet_url + str(item_count)
			self.snippet = self.get_snippet(url)
			if self.snippet != None:
				self.markers_json = self.get_markers_json_from_snippet(self.snippet, ident)
				self.search_results = self.get_search_results_html_from_snippet(self.snippet, ident)
			else:
				url_fail_count += 1
				continue				#don't count data failure if URL failed

			if self.markers_json != None: #url from markers data is required
				self.get_list_item_data(self.markers_json, self.search_results, ident)
			else:
				data_fail_count += 1

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
		self.search_results = None
		self.markers_json = None
		self.snippet = None
		

	