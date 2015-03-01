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

#load local modules
yi = imp.load_source('', 'yelp_item.py')

#####################################################################################
# YELP LIST PAGE CRAWLER - Grab DB data from any Yelp page with a list of items
#	
#	-A so-called 'snippet' URL can be built for a given category, location, and 
#		item start number which returns a large JSON
#	-The main JSON contains an attribute 'markers' which holds basic DB data url,
#		longitude, latitude on the 10 items from start+1 to start+10
#	-regex capture the JSON with the basic data
#	-JSON parse into objects for each Yelp item
#	-URL tail and remaining DB info appears in large text value for another attribute 
#		'search_results' which is parsed to extract this data
#
######################################################################################

class YelpListCrawler:

	def __init__(self, city, state, cat):
		self.city = city.replace(' ', '+')
		self.state = state
		self.cat = cat			#passed to each YelpItem as a category classifier
		self.items = []			#array of YelpItem objects
		self.snippet_url = "http://www.yelp.com/search/snippet?find_desc=" + str(self.cat) + "&find_loc=" + str(self.city) + "%2C+" + str(self.state) + \
								"&start=" 

	def GetURLData(self, url):
		try:
			data = urllib2.urlopen(url)
			return data.read()
		except ValueError:
			return None

	def GetJSONFromURL(self, url_data, ident='No ID'):
		"""
		Params:
			@ident: logging identification
		"""
		#yelp_list_regex = re.compile(r'Controller.*(?P<yelp_list_json>\{"[0-9]+.*\}{3,3})')		#JSON from static list page HTML
		yelp_list_regex = re.compile(r'"markers":.*?(?P<markers>"[0-9]+".*\}{3,3})')				#markers from snippet JSON
		if url_data != None:
			yelp_list_json_match = yelp_list_regex.search(url_data)
			if yelp_list_json_match != None:
				return "{" + yelp_list_json_match.group('markers')
		return None
		
	def GetItemsFromJSON(self, json_str, ident='No ID'):
		"""
		Snippet JSON attribute 'markers' contains url, longitude, latitude for each yelp item on the page
		Create YelpItem instances and fill these 3 details

		Params:
			@json_str: Python dictionary representing a JSON
			@ident: logging identification

		Modify:
			Add newly created YelpItems to member array self.items
		"""
		try:
			json_dict = json.loads(json_str)
		except ValueError:
			print "ERROR: JSON parse failed on " + ident

		for key in json_dict:
			try:
				int(key) 		#json main keys (should be) numbers of each item as they appear in the list		
			except ValueError:
				print "Message: JSON contains non-integer attributes on " + ident

			curr_item = YelpItem(self.cat)
			if 'url' in json_dict[key]:
				curr_item.values['url'] = json_dict[key]['url']
			if 'location' in json_dict[key]:
				if 'longitude' in json_dict[key]['location']:
					curr_item.values['longitude'] = json_dict[key]['location']['longitude']
				if 'latitude' in json_dict[key]['location']:
					curr_item.values['latitude'] = json_dict[key]['location']['latitude']	
			self.items.append(curr_item)

	def Crawl(self, single_list_start_num=None):
		"""
		Crawl Yelp list page(s) for this instances city, state, and category

		Params:
			@single_list_start_num: grabs the items from the single Yelp List page that starts with item number single_list_start_num+1
									if this is omitted then crawl all the list pages available

		TESTING: currently only crawl the first ten items written into the static HTML
		"""
		start = 0
		grab = True

		url_data = None
		json_str = None

		url_fail_count = 0
		json_fail_count = 0

		while grab and start < 50:

			ident = 'start ' + str(start)

			if single_list_start_num != None:
				start = single_list_start_num
				grab = False
			
			if url_fail_count == 4:
				print "Error: 4 failed URL requests...aborting Yelp list page crawl at " + ident

			if json_fail_count == 4:
				print "Message: 4 failed JSON extractions...crawl considerered complete at " + ident
			
			url = self.snippet_url + str(start)

			url_data = self.GetURLData(url)
			if url_data != None:
				json_str = self.GetJSONFromURL(url_data, ident)
			else:
				url_fail_count += 1
				continue				#don't count failed json extraction if URL failed

			if json_str != None:
				self.GetItemsFromJSON(json_str, ident)
			else:
				json_fail_count += 1

			start += 10


	def Flush(self):
		"""
		Empty all YelpItem data captured
		"""
		self.items = []

	def PushItemsToDB(self, conn, table_name='yelp_items'):
		cats = YelpItem.categories
		c = conn.cursor()

		for item in self.items:
			SQL = "INSERT INTO " + table_name + " ("
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
		
		conn.commit()
		c.close()

	