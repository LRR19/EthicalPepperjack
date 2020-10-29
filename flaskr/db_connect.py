import MySQLdb as mariadb
from flaskr.db_credentials import host, user, pw, db

def execute_query(query):

	try:
		# Create database connection
		db_connection = mariadb.connect(host,user,pw,db)

		# Validate connection exists
		if db_connection is None:
			print("No connection to the database found! Have you called connect_to_database() first?")
			return None

		# Validate query isn't empty
		if query is None or len(query.strip()) == 0:
			print("query is empty! Please pass a SQL query in query")
			db_connection.close()
			return None
		
		cursor = db_connection.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		db_connection.commit()
		db_connection.close()
		
		return data

	except Exception as e:
		return (-1, str(e))
