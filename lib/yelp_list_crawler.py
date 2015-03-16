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
#	-This JSON contains an attribute 'markers' which holds basic DB data we care
#		about on the 10 items from start+1 to start+10: url, longitude, latitude:
#
#	"markers" : 
#	{
#		...
#		"105" : 
#			{ 
#			...
#			"url" : "biz/la-ciudad-de-mexico-san-francisco",
#		 	"location" :
#				{ "latitude" : 37.784610600000001, "longitude" : -122.46443840000001}
#			}
#			...
#		...
#	}
#
#	-regex capture the markers JSON
#	-parse the markers json and make YelpItem instances for each of the items with
#		the basic DB info
#
#	GRABBING REMAINING DB INFO:
#	-The main snippet JSON contains an attribute 'search_results' whose value is a
#		long string. Buried in this string is the remaining DB info we care about
#		for the 10 items covered by each snippet page
#	-The url we grabbed from the url attribute above can be used as an anchor to find
#		the rest of the DB info for each item
######################################################################################

class YelpListCrawler:

	def __init__(self, city, state, search_phrase):
		self.city = city.replace(' ', '+')
		self.state = state
		self.search_phrase = search_phrase			#passed to each YelpItem
		self.items = []								#array of YelpItem objects
		self.snippet_url = "http://www.yelp.com/search/snippet?find_desc=" + \
							str(self.search_phrase) + "&find_loc=" + str(self.city) +  \
							"%2C+" + str(self.state) + "&start=" 

	def GetURLData(self, url):
		"""
		Return a string of the the full source of the given url
		"""
		try:
			data = urllib2.urlopen(url)
			data_str = data.read()
			if data_str != None:
				return data_str
			else:
				print "[Err] URL data empty: " + url
				return None
		except ValueError:									#Incorrect URL format
			print "[Err] Invalid URL format: " + url
		except urllib2.URLError:							#Cannot connect to URL
			print "[Err] Could not connect to URL: " + url 

		return None

	"""
	######################
	'markers' JSON methods
	######################
	"""
	def GetMarkersJSONFromSnippetData(self, snippet_json, ident='No ID'):
		"""
		Regex capture the 'markers' JSON string from the full snippet data

		Params:
			@snippet_json: a string of the full snippet JSON
			@ident: logging id

		Return:
			string containing the 'markers' json from the snippet data
		"""
		if snippet_json != None:
			snippet_markers_json_regex = re.compile(r'"markers":.*?(?P<markers>"[0-9]+".*\}{3,3})')
			snippet_markers_regex_match = snippet_markers_json_regex.search(snippet_json)
			if snippet_markers_regex_match != None:
				return "{" + snippet_markers_regex_match.group('markers')
			else:
				print "[Err] No match for 'markers' JSON in snippet data: " + ident
				return None

	def MakeBasicYelpItemsFromMarkersJSON(self, markers_json, ident='No ID'):
		"""
		Snippet JSON attribute 'markers' contains attributes url, longitude, latitude
		Create YelpItem instances and fill these details

		Params:
			@markers_json: a string of the markers json
			@ident: logging id

		Modify:
			Add newly created YelpItems to member array self.items
		"""
		try:
			json_dict = json.loads(markers_json)
		except ValueError:
			print "[Err] Converting 'markers' JSON failed: " + ident

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
				print "[Err] URL attribute missing from 'markers' JSON item " + str(item_no) + ": " + ident

			#capture items location attribute
			if 'location' in json_dict[item_no]:
				if 'longitude' in json_dict[item_no]['location']:
					curr_item.values['longitude'] = json_dict[item_no]['location']['longitude']
				else:
					print "[Err] Location : longitude attribute missing from 'markers' JSON item " + str(item_no) + ": " + ident

				if 'latitude' in json_dict[item_no]['location']:
					curr_item.values['latitude'] = json_dict[item_no]['location']['latitude']	
				else:
					print "[Err] Location : latitude attribute missing from 'markers' JSON item " + str(item_no) + ": " + ident

			else:
				print "[Err] Location attribute missing from 'markers' JSON item " + str(item_no) + ": " + ident

			self.items.append(curr_item)

	"""
	#########################################
	'search_results' and full DB data methods
	#########################################
	"""

	def GetSearchResultsTextFromSnippet(self, snippet_json, ident="No ID"):
		"""
		Grab and return the text value of the 'search_results' attribute of the main snippet JSON

		Params:
			@snippet_json: a string of the full snippet JSON
			@ident: logging id

		Returns:
			a string of the text value of the 'search_results' attribute
		"""
		if snippet_json != None:
			snippet_search_results_value_regex = re.compile(r'"search_results":.*?(?P<search_results>".*),')
			snippet_search_results_regex_match = snippet_search_results_value_regex.search(snippet_json)
			if snippet_search_results_regex_match != None:
				return snippet_search_results_regex_match.group('search_results')
			else:
				print "[Err] No match for 'search_results' text value in snippet data: " + ident
				return None

	"""
	###########################################################
	Operational methods: Crawl, Push to DB, Flush local storage
	###########################################################
	"""
	def Crawl(self, db, start=0, end=None, push_period=100):
		"""
		Crawl Yelp list page(s) for this instances city, state, and search_phrase 

		Params:
			@db: a YelpDBConn object passed to DB push method
			@start: the first snippet url start number to crawl
			@end: the last snippet url start number to crawl (inclusive)
			@push_period: how often to push the populated YelpItems to the DB and flush 
		"""
		item_count = start
		snippet_json = None
		markers_json = None

		url_fail_count = None
		json_fail_count = None

		f = open('search_results.log', 'w')

		while item_count <= end:

			if len(self.items) == push_period:
				self.PushItemsToDB(db)
				self.Flush()
			
			ident = 'start=' + str(item_count)
			
			if url_fail_count == 4:
				print "[Err] 4 URL errors...stopping crawl: " + ident

			if json_fail_count == 4:
				print "[Err] 4 'markers' JSON errors...stopping crawl: " + ident
			
			url = self.snippet_url + str(item_count)
			snippet_json = self.GetURLData(url)
			if snippet_json != None:
				markers_json = self.GetMarkersJSONFromSnippetData(snippet_json, ident)
			else:
				url_fail_count += 1
				continue				#don't count failed json extraction if URL failed

			if markers_json != None:
				self.MakeBasicYelpItemsFromMarkersJSON(markers_json, ident)
			else:
				json_fail_count += 1

			f.write(self.GetSearchResultsTextFromSnippet(snippet_json))
			f.write("\n\n")

			item_count += 10

	def PushItemsToDB(self, db):
		"""
		Push all the YelpItem instance data in self.items to the DB

		Params:
			@db: a YelpDBConn object containing a psycopg2 DB connection
		"""
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

			try:
				c.execute(SQL, item.values)
				db.conn.commit()
			except psycopg2.DataError as e:
				print "[Err] Data error pushing row to DB: " + e.pgerror.replace('ERROR: ', '')

	def Flush(self):
		"""
		Clear all YelpItem data stored in self.items
		"""
		print "[Msg] Flushing " + str(len(self.items)) + " local item's data"
		self.items = []
		

	