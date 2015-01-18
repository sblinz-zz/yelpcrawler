# The Everything Pin

## Project Description

Given a dropped map pin, return itemized data from multiple categories describing the area around the pin. Categories can include:
-*Restaurants & Bars*
-*Points of Interest* (museums, landmarks, parks)
-*Census data* (housing, crime, income, etc.)
-*Education* (schools, universities)
-*Services*

**Note:** This project is nothing more than an excuse to develop my SQL skills and learn some new Python tricks and libraries, especially web crawling. For this reason,
we start with crawling and parsing URLs even in cases where an API exists (e.g., Yelp or Googple Places) and write SQL queries directly instead of relying on an ORM. After
this we might switch to APIs and ORMs for practice with that.

## Design Notes

### Searching

Support pin drops in a predefined collection of cities. Crawl category data for each city beforehand and store in database, with regular updating. To returning specific data in real-time,
define a density threshold for each category. Given a pin drop, query each categories entries with an increasing radial geofence until at least the threshold number of entries is 
captured (or a practical maximum radius is reached).

### Data Collection and Management

-Background and real-time data collection through our own Python web crawler (for practice!)
-Later connect through common web APIs directly (Yelp, Google Places)
-PostgreSQL database; direct querying at first (for practice!), later through an ORM

### Front-end
Web UI with Google maps portal for pin dropping and results summary.

### Back-end
Python scripts for data crawling, push/pull to database, and interfacing with web UI.

### Feature Planning

We start with the Restaurants & Bars category first and go from there.