from flaskr import app, db_connect
from flask import render_template, request, redirect, jsonify, url_for, flash, session
from .forms import LoginForm, SignUpForm

from .db_connect import execute_query

# Route to the login page
@app.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


# Route to the signup page
@app.route('/signup')
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)


@app.route('/search_category', methods=['GET', 'POST'])
def search_category():
    if request.method == 'GET':
        return render_template('search_category.html')

    elif request.method == 'POST':
        user_data = request.form
        ethical_category = user_data['search_category']

        query_categories = """SELECT * FROM ethical_categories WHERE name =
        \'%s\';""" %(ethical_category)

        data = execute_query(query_categories)

        query_ingredients = """ SELECT ingredients.name
                                FROM ingredients
                                INNER JOIN(
                                    SELECT ia.alt_ingredient_id
                                    FROM ingredient_alts ia
                                    WHERE ia.ingredient_id = (
                                        SELECT ingredients.id FROM ingredients
                                        INNER JOIN ingredients_concerns ON ingredients.id = ingredients_concerns.ingredient_id
                                        INNER JOIN ethical_concerns ec on ingredients_concerns.concern_id = ec.id
                                        INNER JOIN ethical_categories e on ec.category_id = e.id
                                        WHERE e.id = %d )) alts
                                ON ingredients.id = alts.alt_ingredient_id; """ %(data[0][0])

        data2 = execute_query(query_ingredients)
        return render_template('search_category.html', name=ethical_category,
                               ingredients=data2)


# This will be all of the routes for the recipe book function. There will be a
# Get to get the current users recipe
# book. Delete will remove a recipe.

@app.route('/recipe_book')
def recipebook():
    return render_template('recipe_book/user.html')

# Route to handle the display of ingredients after searching for a recipe.
# Recipe name is the input and will return list of all ingredients
@app.route('/recipe_display')
def recipe_display():
#   Get the recipe name  from the search bar
    recipe_name = request.args.get("recipe_name")

    # Use session cookie if name not in the url
    if recipe_name == None:
        recipe_name = session['recipe_name_alt']

#    print(recipe_name)
#    recipe_name = "tomato soup"
#   Find the associated recipe ID with the recipe name
    id_query = "SELECT id FROM recipes WHERE name =\'%s\';" %(recipe_name)
    result = execute_query(id_query)
    print(type(result))
    #   Convert result tuple to integer
    recipe_id = result[0][0]
    query = "SELECT i.id, i.name, i.description, i.origin FROM ingredients AS i\
    INNER JOIN recipes_ingredients ON i.id = recipes_ingredients.ingredient_id\
    WHERE recipes_ingredients.recipe_id = %d;" %(recipe_id)
    #   Convert result tuple to list and then just get the first element of the tuple
    ingredient_list = list(execute_query(query))
    #   ingredient_list =[item for t in result for item in t]
    #   Pass the search query and the list of ingredients to the new html for display.
    return render_template('recipe_display.html', name=recipe_name,recipeID=recipe_id, ingredients=ingredient_list)


@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    if request.method == 'GET':
        return render_template('search_recipe.html')

    elif request.method == 'POST':
        user_data = request.form
        recipe_name = user_data['search_recipe_name']

        query = """SELECT name,id FROM recipes WHERE name =
        \'%s\';""" %(recipe_name)

        recipes = list(execute_query(query))


        if(recipes):
            return render_template('search_recipe.html', names=recipes)
        else:
            error_message=[("No recipes found, please try again",)]
            return render_template('search_recipe.html', names=error_message)


@app.route('/user_recipebook')
def user_recipebook():
    username = "KC"
    recipe_list = ['tomato soup', 'tuna sandwich', 'mashed potatoes']

    return render_template('recipe_book/user.html', name=username, recipes=recipe_list)

@app.route('/alternatives', methods=['GET','POST'])
def alternatives():

    if request.method == 'GET': # Show alternatives

        session['recipe_id_alt'] = int(request.args.get('recipeID'))
        session['ingredient_id_alt'] = int(request.args.get('ingredientID'))
        session['recipe_name_alt'] = request.args.get('recipe_name')

        query_name = """ SELECT name, description
                         FROM ingredients
                         WHERE id = %d """ %(session['ingredient_id_alt'])

        ingredient = list(execute_query(query_name))[0]

        query_ingredients = """ SELECT ingredients.id,
                                       ingredients.name,
                                       ingredients.description
                                FROM ingredients
                                INNER JOIN(
                                    SELECT ia.alt_ingredient_id
                                    FROM ingredient_alts ia
                                    WHERE ia.ingredient_id = %d) alts
                                ON ingredients.id = alts.alt_ingredient_id """ %(session['ingredient_id_alt'])

        alternative_list = list(execute_query(query_ingredients))

        unethical_reason = "water intensive to produce and high in greenhouse gas emissions."

        return render_template('alternative_display.html', ingredient=ingredient, unethical=unethical_reason, alternatives = alternative_list)

    else: # POST request to switch ingredient

        recipe_id = session['recipe_id_alt']

        ingredient_id = session['ingredient_id_alt']

        new_ingredient_id = int(request.form['ingredient_id'])

        query_recipe_ing = """UPDATE recipes_ingredients
                              SET ingredient_id = %d
                              WHERE recipe_id = %d
                              AND ingredient_id = %d; """ %(new_ingredient_id,recipe_id,ingredient_id)

        update = execute_query(query_recipe_ing)

        return redirect(url_for('recipe_display'))



# @app.route('/home', methods=['GET','POST'])
# def home():

# 	# Sample query
# 	# query = """SELECT * FROM table JOIN table.id = table2.id WHERE table.id = %d;""" %(table_id)

# 	# Execute query
# 	# results = db_connect.execute_query(query)

@app.errorhandler(404)
def pageNotFound(error):
	return render_template('404.html', title='Page Not Found')

@app.errorhandler(500)
def majorError(error):
	return render_template('500.html', title='Major Error')
