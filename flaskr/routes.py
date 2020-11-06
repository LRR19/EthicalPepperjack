from flaskr import app
from flask import render_template, request, redirect, jsonify, url_for, flash, session
from flask_mysqldb import MySQL
from .db_connect import *


mysql = MySQL(app)


@app.route('/')
def index():

    return render_template('base.html', title='test')


##This will be all of the routes for the recipe book function. There will be a Get to get the current users recipe
##book. Delete will remove a recipe.

@app.route('/recipebook')
def recipebook():

    return render_template('recipe_book/user.html')

# Route to handle the display of ingredients after searching for a recipe.
# Recipe name is the input and will return list of all ingredients
@app.route('/recipesearch')
def search_for_recipe():
#   Get the recipe name  from the search bar
#   recipe_name = request.args.get("recipe_name")
    recipe_name = "tomato soup"#   
#   Find the associated recipe ID with the recipe name
    id_query = "SELECT id FROM recipes WHERE name =\'%s\';" %(recipe_name)    
    result = execute_query(id_query)
#   Convert result tuple to integer
    recipe_id = result[0][0]    
    query = "SELECT ingredients.name, ingredients.description, ingredients.origin FROM ingredients\
    INNER JOIN recipes_ingredients ON ingredients.id = recipes_ingredients.ingredient_id\
    WHERE recipes_ingredients.recipe_id = %d;" %(recipe_id)
#   Convert result tuple to list and then just get the first element of the tuple      
    ingredient_list = list(execute_query(query))        
#    ingredient_list =[item for t in result for item in t]
#   Pass the search query and the list of ingredients to the new html for display.
    return render_template('recipe_display.html', name=recipe_name, ingredients=ingredient_list)



    

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