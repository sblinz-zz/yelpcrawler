# Yelp Crawler

## Project Description

A non-API based Yelp web crawler. Created to practice some Python tricks and libraries for web crawling. Purposefully avoid Yelp's API to crawl Yelp URLs.

## Design

For each results page (listing 10 items for a given search phrase in a specified city/location) Yelp passes a JSON called `snippet`. This JSON contains attributes with basic data on each of the items. Another attirbute contains a large HTML string which can be parsed using the basic attributes to obtain the rest of the relevent item data.

These `snippet` JSONs can be accessed by URLs of the form 

`http://www.yelp.com/search/snippet?find_desc=Restaurants&find_loc=San%20Francisco%2C%20CA&start=10`

The value passed to the `start` parameter can be used to iterate through all the items returns for the given search phrase and location.

## Operation

Each instance of `CityCrawler` can capture data on any number of items across any number of search phrases. See `sql\tables\yelp_items.sql` or the definition of `YelpItem` for details on data captured for each item.

While crawling, each `YelpListCrawler` instance can periodically push scraped data to a PostgreSQL DB