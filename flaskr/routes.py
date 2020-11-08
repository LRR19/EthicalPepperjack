from flaskr import app, db_connect
from flask import render_template, request, redirect, jsonify, url_for, flash, session

from .db_connect import *


@app.route('/')
def index():
    return render_template('base.html', title='test')


@app.route('/search_category', methods=['GET', 'POST'])
def search_category():
    if request.method == 'GET':
        return render_template('search_category.html')

    elif request.method == 'POST':
        user_data = request.form
        ethical_category = user_data['search_category']

        query_categories = """SELECT * FROM ethical_categories WHERE name = 
        %s;"""

        data = execute_query(query_categories, ethical_category)

        query_ingredients = """SELECT ingredients.name 
        FROM ingredients
        WHERE ingredients.id = (
            SELECT ia.alt_ingredient_id 
            FROM ingredients
            INNER JOIN ingredient_alts ia on ingredients.id = ia.ingredient_id
            WHERE ia.ingredient_id = (
                SELECT ingredients.id FROM ingredients
                INNER JOIN ingredients_concerns ON ingredients.id = ingredients_concerns.ingredient_id
                INNER JOIN ethical_concerns ec on ingredients_concerns.concern_id = ec.id
                INNER JOIN ethical_categories e on ec.category_id = e.id
                WHERE e.name = %s));"""
        data2 = execute_query(query_ingredients, str(data[0][1]))
        return render_template('search_category.html', name=ethical_category,
                               ingredients=data2)


# This will be all of the routes for the recipe book function. There will be a
# Get to get the current users recipe
# book. Delete will remove a recipe.

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