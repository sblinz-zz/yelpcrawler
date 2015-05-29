##############################################################################################
# The Everything Pin Project
# 
# File: lib\db.py
# Desc: DB structures
##############################################################################################

"""
##########################
Database Data Structures
##########################
"""

private = imp.load_source('', 'private.py')

class DBConnectException(Exception):
	pass

#Base database connection class
class DBConnection:

	def connect(self):
		print "[Msg] Connecting to database..."
		self.conn = psycopg2.connect(("dbname='{}' user='{}' password='{}' host='{}' port='{}'").format(private.DB_NAME, private.DB_USERNAME, private.DB_PASSWORD, private.DB_HOST, private.DB_PORT))
		print "[Msg] Connected to database successfully"
		
	def close(self):
		print "[Msg] Closing connection to database"
		self.conn.close()

#Wrapper for psycopg2 connection object and table name
class YelpDBConn(DBConnection):

	def __init__(self, table='yelp_items'):
		self.connect()
		self.table = table
