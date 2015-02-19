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
from bs4 import BeautifulSoup	#HTML parse

#load local modules
yi = imp.load_source('', 'yelp_item.py')

#####################################################################################
# YELP LIST PAGE CRAWLER - Grab DB data from any Yelp page with a list of items
#
#	-Each Yelp list page has a JSON at the bottom of the page containing a tail URL,
#		longitude/latitude for each of the items on the page
#	-regex capture the inner JSON containing this data
#	-JSON parse into objects for each Yelp item
#	-URL tail appears in the HTML anchor of each items text and img link: use it to
#		get remaining YelpItem object details
#
######################################################################################

class YelpListCrawler:

	def __init__(self, city, state, cat):
		self.city = city
		self.state = state
		self.cat = cat			#passed to each YelpItem as a category classifier
		self.items = []			#array of YelpItem objects
		self.search_url = "http://www.yelp.com/search?find_desc=" + self.cat + "&find_loc=" + self.city + "%2C+" + self.state + "&ns=1#start=" 

	def GetHTMLFromURL(self, url):
		try:
			data = urllib2.urlopen(url)
			return data.read()
		except ValueError:
			print "Error: Invalid URL request"

	def GetJSONFromHTML(self, html):
		yelp_list_regex = re.compile(r'Controller.*(?P<yelp_list_json>\{"1.*\}{3,3})')
		if(html != None):
			yelp_list_json_match = yelp_list_regex.search(html)
			if yelp_list_json_match != None:
				return yelp_list_json_match.group('yelp_list_json')
		return None
		
	def GetItemsFromJSON(self, json_str):
		"""
		Yelp list page JSON contains url, longitude, latitude for each yelp item on the page
		Create YelpItem instances and fill these 3 details from a JSON dictionary

		Params:
			@json: Python dictionary representing inner JSON from bottom of Yelp list page HTML

		Modify:
			Add newly created YelpItems to member array self.items
		"""
		json_dict = json.loads(json_str)
		for key in json_dict:
			try:
				int(key) 		#json main keys (should be) numbers of each item as they appear in the list		
			except ValueError:
				continue

			curr_item = YelpItem(self.cat)
			if 'url' in json_dict[key]:
				curr_item.details['url'] = json_dict[key]['url']
			if 'location' in json_dict[key]:
				if 'longitude' in json_dict[key]['location']:
					curr_item.details['longitude'] = json_dict[key]['location']['longitude']
				if 'latitude' in json_dict[key]['location']:
					curr_item.details['latitude'] = json_dict[key]['location']['latitude']	
			self.items.append(curr_item)

	def Crawl(self, single_list_start_num=None):
		"""
		Crawl Yelp list page(s) for this instances city, state, and category

		Params:
			@single_list_start_num: grabs the items from the single Yelp List page that starts with item number single_list_start_num+1
									if this is omitted then crawl all the list pages available
		"""
		if single_list_start_num != None:
			url = self.search_url + str(single_list_start_num)
			html = self.GetHTMLFromURL(url)
			page_json = self.GetJSONFromHTML(html)
			self.GetItemsFromJSON(page_json)