import psycopg2
import urllib2

def insert_new_restaurant(name):
  conn = psycopg2.connect(("dbname='{}' user='{}' host='{}' password='{}' port='{}'").format(DB_NAME, 
                DB_USERNAME, DB_HOST, DB_PASSWORD, DB_PORT))
  cursor = conn.cursor()
  cursor.execute("insert into restaurants (name) values ('%s')" % (name))
  conn.commit()

def read_all_restaurant_names():
  conn = psycopg2.connect(("dbname='{}' user='{}' host='{}' password='{}' port='{}'").format(DB_NAME, 
                DB_USERNAME, DB_HOST, DB_PASSWORD, DB_PORT))
  cursor = conn.cursor()
  cursor.execute("SELECT name FROM restaurants")
  return cursor.fetchall()

def get_web_page(url):
  data = urllib2.urlopen(url)
  print data.read()