##############################################################################################
# Yelp Crawler
# 
# File: yelp_list_crawler.py
# Desc: crawler class for any yelp list page; creates an array of YelpItem objects
##############################################################################################

#packages
import urllib2 					#URL capture
import re 						#regex's
import json						#parsing json string <-> python dictionary
import psycopg2					#DB connection
from bs4 import BeautifulSoup 	#html parser

#load local modules
import yelp_item as yi

#####################################################################################
# YELP LIST PAGE CRAWLER - Grab DB data from Yelp 'snippet' pages
#	
#	GRABBING BASIC DB INFO:
#	-A so-called 'snippet' URL can be built for a given category, location, and 
#		item start number which returns a JSON.
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
#	-The parent snippet JSON contains an attribute 'search_results' whose value is a
#		long string with html that contains the remaining DB data we need for each item
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
		self.snippet = None					#snippet json string for extracting markers json and search_results attributes
		self.markers_dict = None			#markers json dictionary
		self.search_results_html = None		#search_results html string

		#Logging/Debugging
		self.log = open('yelpcrawler.log', 'w')

	########################################
	#Scrape URL Methods
	#	-snippet JSON
	#	-markers JSON from snippet
	#	-search_results html from snippet
	########################################
	
	def get_snippet(self, url):
		"""
		@url is identifier for logging

		Returns:
			snippet json as a string
		"""
		try:
			data = urllib2.urlopen(url)
			data_str = data.read()
			if data_str != None:
				return data_str
			else:
				print("[Err] URL data empty - " + url)
				return None
		except ValueError:									#Incorrect URL format
			print("[Err] Invalid URL format - " + url)
		except urllib2.URLError:							#Cannot connect to URL
			print("[Err] Could not connect to URL - " + url) 

		return None

	def get_markers_dict_from_snippet(self, snippet, ident='No ID'):
		"""
		Regex capture the markers JSON as a string from the full snippet string

		Params:
			@snippet: a string of the full snippet json
			@ident: logging identification

		Return:
			markers json as a string (it is converted to and used as a dictionary in )
		"""
		if snippet != None:
			snippet_markers_json_regex = re.compile(r'"markers":.*?(?P<markers>"[0-9]+".*\}{3,3})')
			snippet_markers_json_regex_match = snippet_markers_json_regex.search(snippet)
			if snippet_markers_json_regex_match != None:
				markers_string =  "{" + snippet_markers_json_regex_match.group('markers')
			else:
				print("[Err] No match for markers in snippet - " + ident)
				return None

			#create markers dictionary to iterate over this lists items
			try:
				markers_dict = json.loads(markers_string)
				return markers_dict
			except ValueError:
				print("[Err] Converting 'markers' JSON failed - " + ident)
				return

	def get_search_results_html_from_snippet(self, snippet, ident="No ID"):
		"""
		Regex campture the the search_results attribute of the snippet json

		Params:
			@snippet: a string of the full snippet json
			@ident: logging identification

		Returns:
			search_results attribute value as a string with correct html
		"""
		if snippet != None:
			snippet_search_results_html_regex = re.compile(r'"search_results":[ ]*"(?P<search_results>.*?)",', re.DOTALL)
			snippet_search_results_html_regex_match = snippet_search_results_html_regex.search(snippet)
			if snippet_search_results_html_regex_match != None:
				search_results = snippet_search_results_html_regex_match.group('search_results')
				search_results = search_results.replace('\u003c', '<')
				search_results = search_results.replace('\u003e', '>')
				search_results = search_results.replace('\u0026', '&')
				search_results = search_results.replace('\u2019', "'")
				search_results = search_results.replace('\\n', '\n')
				search_results = search_results.replace('\\"', '"')
				return search_results

		else:
			print("[Err] No match for search_results attribute in snippet - "  + ident)
			return None

	########################################
	#Get List Item Data Methods
	#	-parent method
	#	-markers item data (basic data)
	#	-search results item data parent
	########################################

	def get_list_item_data(self, markers_dict, search_results, ident="No ID"):
		"""
		Snippet markers attribute is a JSON with url and location data for each item
		Snippet search_results attribute is HTML with remaining data for each item

		Parent method iterating over all items in markers and call resepective methods to
		fill data from markers and search_results

		Params:
			@markers_dict: markers JSON as a dictionary
			@search_results: search_results HTML as a string
			@ident: logging id

		Modify:
			Add filled YelpItem instance to self.items for each item in markers JSON
		"""

		#iterate over item numbers in the markers json dictionary
		#skip marker attributes not identifying an item
		for item_no in markers_dict:
			try:
				int(item_no)	
			except ValueError:
				continue

			curr_item = yi.YelpItem(self.search_phrase)
			self.get_item_data_from_markers_item_dict(curr_item, markers_dict[item_no], ident)
			self.get_item_data_from_search_results_html(curr_item, search_results, ident)
			self.items.append(curr_item)


	def get_item_data_from_markers_item_dict(self, yelp_item, markers_item_dict, ident='No ID'):
		"""
		Each markers item attribute contains attributes url, longitude, latitude

		Params:
			@yelp_item: YelpItem instance to fill
			@markers_item_dict: a dictionary of the given item in the markers dictionary
			@ident: logging id

		Modify:
			Fill url and location data for given YelpItem instance
		"""

		#capture items URL attribute
		if 'url' in markers_item_dict:
			yelp_item.values['url'] = markers_item_dict['url']
		else:
			print("[Err] URL attribute missing from 'markers' JSON item - : " + ident + " : item no. " + str(item_no))

		#capture items location attribute
		if 'location' in markers_item_dict:
			if 'longitude' in markers_item_dict['location']:
				yelp_item.values['longitude'] = markers_item_dict['location']['longitude']
			else:
				print("[Err] Location : longitude attribute missing from 'markers' JSON item - " + ident + " : item no. " + str(item_no)) 

			if 'latitude' in markers_item_dict['location']:
				yelp_item.values['latitude'] = markers_item_dict['location']['latitude']	
			else:
				print("[Err] Location : latitude attribute missing from 'markers' JSON item - " + ident + " : item no. " + str(item_no))

		else:
			print("[Err] Location attribute missing from 'markers' JSON item - " + ident + " : item no. " + str(item_no))

	def get_item_data_from_search_results_html(self, yelp_item, search_results, ident="No ID"):
		"""
		search_results html contains remaining data to grab, anchored by item url
		parse with beautifulsoup for the given YelpItem instance

		Params:
			@yelp_item: YelpItem instance to fill
			@search_results: a string of the search_results clean html
			@ident: logging identification

		Modify:
			Add data values from search_results to YelpItem instance
		"""
		url = yelp_item.values['url']
		if url != None:
			soup = BeautifulSoup(search_results)

			#Find the name attribute using <a href="url" class="biz-name">...</a>
			#Use the <a class="biz-name"> tag to locate the two main <div> tags for this item
			a_biz_name = soup.find('a', href=url, class_='biz-name')
			div_main_attributes = a_biz_name.find_parent("div", class_="main-attributes")
			div_secondary_attributes = div_main_attributes.find_next_sibling("div", class_="secondary-attributes")
			
			#Name
			yelp_item.values['name'] = a_biz_name.string

			#Address
			#
			#<div class="secondary-attributes">
			#	<address>
			#		street adddress
			#		<br>city, state</br>
			#	</address>
			#</div>
			street = div_secondary_attributes.address.contents[0].replace("\n", "").replace("            ", "")
			city_state = div_secondary_attributes.address.br.string.replace("\n", ""))
			yelp_item.values['address'] = street + ", " + city_state

			#Rating

			#Price

			#Phone

	#######################################
	#Crawl Operations Methods
	#	-main API method to crawl
	#	-push item to DB
	#	-flush local item data
	########################################

	def crawl(self, db, start=0, end=None, push_period=100):
		"""
		main API method
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
					print("[Err] Data error pushing row to DB - " + e.pgerror.replace('ERROR: ', ''))
			
			ident = 'start=' + str(item_count)
			
			if url_fail_count == 4:
				print("[Err] 4 URL errors...stopping crawl - " + str(ident))

			if data_fail_count == 4:
				print ("[Err] 4 insufficient data errors...stopping crawl - " + str(ident))
			
			url = self.snippet_url + str(item_count)
			self.snippet = self.get_snippet(url)
			if self.snippet != None:
				self.markers_dict = self.get_markers_dict_from_snippet(self.snippet, ident)
				self.search_results_html = self.get_search_results_html_from_snippet(self.snippet, ident)
				self.log.write(self.search_results_html)
			else:
				url_fail_count += 1
				continue				#don't count data failure if URL failed

			if self.markers_dict != None: #url from markers data is required
				self.get_list_item_data(self.markers_dict, self.search_results_html, ident)
			else:
				data_fail_count += 1

			item_count += 10

	def push_items_to_db(self, db):
		print "[Msg] Pushing " + str(len(self.items)) + " items to DB"
		cats = yi.YelpItem.cats
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
		print("[Msg] Flushing " + str(len(self.items)) + " item's local data")
		self.items = []
		self.search_results = None
		self.markers_json = None
		self.snippet = None
		

	