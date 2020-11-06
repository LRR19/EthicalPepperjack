from flaskr import app
from flask import render_template, request, redirect, jsonify, url_for, flash, session


@app.route('/')
def index():

	return render_template('base.html', title='test')

# @app.route('/home', methods=['GET','POST'])
# def home():

# 	# Sample query
# 	# query = """SELECT * FROM table JOIN table.id = table2.id WHERE table.id = %d;""" %(table_id)

# 	# Execute query
# 	# results = db_connect.execute_query(query)

# @app.errorhandler(404)
# def pageNotFound(error):
# 	return render_template('404.html', title='Page Not Found')

# @app.errorhandler(500)
# def majorError(error):
# 	return render_template('500.html', title='Major Error')