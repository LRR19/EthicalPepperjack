from flaskr import app, db_connect
from flask import render_template, request, redirect, jsonify, url_for, flash,\
    session
from .forms import LoginForm, SignUpForm
from .models import User
from flask_login import login_user, logout_user, \
    login_required, current_user
from .db_connect import execute_query
from werkzeug.security import generate_password_hash, check_password_hash

# Route to the login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = execute_query(
            """SELECT id, username, f_name, l_name, email, password FROM users
                WHERE username = \'%s\';""" % form.username.data)
        user_list = list(user)
        if user_list:
            if check_password_hash(user_list[0][5], form.password.data):
                user_obj = User(id=user_list[0][0], username=user_list[0][1], f_name=user_list [0][2], l_name=user_list [0][3],
                email=user_list[0][4], password=user_list[0][5])
                login_user(user_obj)
                return redirect('/profile')
            else:
                flash("Password is incorrect")
        else:
            flash("Account is not found")
    return render_template('login.html', form=form)


# Route to the signup page
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = execute_query(
            """SELECT id, username, password FROM users
                WHERE username = \'%s\';""" % form.username.data)
        if user:
            flash("There is already an account with that name.")
        else:
            hashed_password = generate_password_hash(form.password.data)
            query = """INSERT INTO users
                        (username, f_name, l_name, email, password)
                        VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')""" \
                    % (form.username.data, form.f_name.data,
                       form.l_name.data, form.email.data, hashed_password)
            try:
                insert = execute_query(query)
                return_id = list(
                    execute_query("""SELECT id FROM users
                                      WHERE username = \'%s\';"""
                                  % form.username.data))
                user_obj = User(id=return_id[0][0], username=form.username.data, f_name=form.f_name.data, l_name=form.l_name.data,
                email=form.email.data, password=hashed_password)
                login_user(user_obj)
                flash("You have successfully signed up!")
                return redirect('/profile')
                # alert successful
            except:
                # alert not successful
                flash("The username or email has already been used!")
    return render_template('signup.html', form=form)


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return render_template('profile_error.html')
    ##else we display the current user information
    return render_template('profile.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Account has been logged out")
    return redirect('/')


# Route for guest (restrict saving recipes)
@app.route('/guest')
def guest():
    return render_template('search_recipe.html')


# Search for an ethical concern and displays alternative ingredients
@app.route('/search_category', methods=['GET', 'POST'])
def search_category():
    if request.method == 'GET':
        return render_template('search_category.html')

    elif request.method == 'POST':
        user_data = request.form
        ethical_category = user_data['search_category']

        # Find the associated information with the name of the ethical concern
        query_categories = """SELECT * FROM ethical_categories WHERE name =
        \'%s\';""" % ethical_category

        # get tuple results: name of ethical concern
        data = execute_query(query_categories)

        # Find the alternative ingredient(s) associated  with the name of the
        # ethical concern
        query_ingredients = """ SELECT ingredients.name
                                FROM ingredients
                                INNER JOIN(
                                    SELECT ia.alt_ingredient_id
                                    FROM ingredient_alts ia
                                    WHERE ia.ingredient_id = (
                                        SELECT ingredients.id FROM ingredients
                                        INNER JOIN ingredients_concerns
                                        ON ingredients.id =
                                        ingredients_concerns.ingredient_id
                                        INNER JOIN ethical_concerns ec
                                        on ingredients_concerns.concern_id =
                                        ec.id
                                        INNER JOIN ethical_categories e
                                        on ec.category_id = e.id
                                        WHERE e.id = %d )) alts
                                ON ingredients.id = alts.alt_ingredient_id; """ \
                            % (data[0][0])

        # get tuple results: name of alternative ingredient
        alts_ingredient_query = execute_query(query_ingredients)

        return render_template('search_category.html', name=ethical_category,
                               ingredients=alts_ingredient_query)


# This will be all of the routes for the recipe book function. There will be a
# Get to get the current users recipe
# book. Delete will remove a recipe.
@app.route('/user_recipebook')
def user_recipebook():
    if not current_user.is_authenticated:
        return render_template('recipe_book/error.html')

    current_user_id = current_user.get_id()

    query_recipe_book = "SELECT r.id, r.name, r.description " \
                        "FROM recipes as r INNER JOIN users_recipes " \
                        "ON r.id = users_recipes.recipe_id " \
                        "WHERE users_recipes.user_id = %d;" % current_user_id

    recipe_list = list(execute_query(query_recipe_book))

    return render_template('recipe_book/user.html', recipes=recipe_list)


@app.route('/add_recipe_to_user_book', methods=['POST'])
def add_recipe_to_user_book():
    if not current_user.is_authenticated:
        return redirect(url_for('recipe_book/error.html'))
    else:
        current_user_id = current_user.get_id()
        recipe_id = int(request.form['recipe_id'])

        query_add_to_recipe_book = "INSERT INTO users_recipes " \
                                   "(user_id,recipe_id) VALUES (%d,%d);" \
                                   % (current_user_id, recipe_id)

        execute_query(query_add_to_recipe_book)

        return redirect(url_for('user_recipebook'))


@app.route('/delete_recipe_from_user_book', methods=['POST'])
def delete_recipe_from_user_book():
    current_user_id = current_user.get_id()
    recipe_id = int(request.form['recipe_id'])

    query_remove_from_recipe_book = "DELETE FROM users_recipes " \
                                    "WHERE user_id = %d AND recipe_id = %d;" \
                                    % (current_user_id, recipe_id)

    execute_query(query_remove_from_recipe_book)

    return redirect(url_for('user_recipebook'))


# Route to handle the display of ingredients after searching for a recipe.
# Recipe name is the input and will return list of all ingredients
@app.route('/recipe_display')
def recipe_display():
    #   Get the recipe name from the search bar
    recipe_name = request.args.get("recipe_name")

    # Use session cookie if name not in the url. Else, add recipe name to session cookie
    if recipe_name is None:
        recipe_name = session['recipe_name']
    else:
        session['recipe_name'] = recipe_name

    
    id_query = "SELECT id FROM recipes WHERE name =\'%s\';" % recipe_name
    result = execute_query(id_query)
    #   Convert result tuple to integer
    recipe_id = result[0][0]
    #   Add recipe id to session cookie
    session['recipe_id'] = recipe_id
    
    #   Select all ingredients in recipes_ingredients  and their concerns for display
    query = "SELECT i.id, i.name, i.description, i.origin, ec.name, ec.description " \
            "FROM ingredients AS i " \
            "LEFT JOIN recipes_ingredients AS ri ON i.id = ri.ingredient_id " \
            "LEFT JOIN ingredients_concerns AS ic ON i.id = ic.ingredient_id " \
            "LEFT JOIN ethical_concerns AS ec ON ic.concern_id = ec.id " \
            "WHERE ri.recipe_id = %d;" % recipe_id

    #   Convert result tuple to list
    ingredient_list = list(execute_query(query))
    
    
    #   Pass the search query and the list of ingredients to
    #   the new html for display.
    return render_template('recipe_display.html', name=recipe_name,
                           recipe_id=recipe_id, ingredients=ingredient_list)


# Displays a list of all recipes or a specific recipe after searching for one.
@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    if request.method == 'GET':

        # Find the associated recipe name, description and rank
        recipe_query = """SELECT name, description, ethical_ranking
                           FROM recipes;"""

        # Convert result tuple to list and get the first element of the tuple
        display_recipes = list(execute_query(recipe_query))

        return render_template('search_recipe.html',
                               recipe_list=display_recipes)

    # Displays searched recipe
    elif request.method == 'POST':
        user_data = request.form
        recipe_name = user_data['search_recipe_name']

        # Find the associated recipe description and rank with the recipe name
        query = """SELECT name, description, ethical_ranking
                    FROM recipes WHERE name = \'%s\';""" % recipe_name

        recipes = list(execute_query(query))

        if recipes:
            return render_template('search_recipe.html', recipe_list=recipes)
        else:
            error_message = [("No recipes found, please try again",)]
            return render_template('search_recipe.html',
                                   recipe_list=error_message)


@app.route('/alternatives', methods=['GET', 'POST'])
def alternatives():
    if request.method == 'GET':  # Show alternatives

        session['recipe_id_alt'] = int(request.args.get('recipe_id'))
        session['ingredient_id_alt'] = int(request.args.get('ingredient_id'))
        session['recipe_name'] = request.args.get('recipe_name')

        query_name = """ SELECT name, description
                         FROM ingredients
                         WHERE id = %d """ % (session['ingredient_id_alt'])

        ingredient = list(execute_query(query_name))[0]

        query_ingredients = """ SELECT ingredients.id,
                                       ingredients.name,
                                       ingredients.description
                                FROM ingredients
                                INNER JOIN(
                                    SELECT ia.alt_ingredient_id
                                    FROM ingredient_alts ia
                                    WHERE ia.ingredient_id = %d) alts
                                ON ingredients.id = alts.alt_ingredient_id """ \
                            % (session['ingredient_id_alt'])

        alternative_list = list(execute_query(query_ingredients))

        return render_template('alternative_display.html',
                               ingredient=ingredient,
                               alternatives=alternative_list)

    else:  # POST request to switch ingredient

        query_recipe_ing = """UPDATE recipes_ingredients
                              SET ingredient_id = %d
                              WHERE recipe_id = %d
                              AND ingredient_id = %d; """ \
                           % (int(request.form['ingredient_id']),
                              session['recipe_id_alt'],
                              session['ingredient_id_alt'])

        update = execute_query(query_recipe_ing)

        return redirect(url_for('recipe_display'))


@app.route('/add_ingredients', methods=['GET', 'POST'])
def add_ingredients():

    print("In here")

    if request.method == "GET":

        if request.args.get('ingredient_name'):

            query = """SELECT i.id, i.name, i.description, rankings.ranking
                        FROM ingredients i
                        LEFT JOIN ingredients_concerns ic
                        ON i.id = ic.ingredient_id
                        LEFT JOIN ethical_concerns ec ON ic.concern_id = ec.id
                        LEFT JOIN rankings ON ec.ranking_id = rankings.id
                        WHERE i.name LIKE (\'%%%s%%\');""" \
                    % (request.args.get('ingredient_name'))

            ingredients = list(execute_query(query))

            visible_prop = "block" if len(ingredients) == 0 else "none"

        else:

            ingredients = []
            visible_prop = "none"

        

        return render_template('add_ingredient.html', ingredients=ingredients, recipe=session['recipe_name'], visible_prop=visible_prop)

    if request.method == 'POST':

        if 'submit_ing_id' in request.form: # Adding ingredient to recipe

            query = """INSERT INTO recipes_ingredients
                        (recipe_id, ingredient_id, quantity, unit)
                        VALUES (%d,%d,%d,\'%s\');""" \
                    % (int(session['recipe_id']), int(request.form['submit_ing_id']), int(request.form['quantity']), request.form['unit'])

            execute_query(query)

            return redirect(url_for('recipe_display'))

        else:
            
            if request.form['ingredient_name'] == '':
                flash("Unable to add ingredient without a name!")
                return redirect(url_for('add_ingredients'))

            if request.form['ingredient_desc'] == '':
                desc = 'none'
            else:
                desc = request.form['ingredient_desc']

            if request.form['ingredient_origin'] == '':
                origin = 'none'
            else:
                origin = request.form['ingredient_origin']

            # Add ingredient to database
            query = """INSERT INTO ingredients
                        (name,description,origin)
                        VALUES(\'%s\',\'%s\',\'%s\');""" \
                        % (request.form['ingredient_name'], desc, origin)

            execute_query(query)

            flash("Thanks! " + request.form['ingredient_name'] + " has been added to the database for review!")

            return redirect(url_for('add_ingredients'))
        


@app.route('/', methods=('GET', 'POST'))
def homepage():
    form = LoginForm()
    if form.validate_on_submit():
        user = execute_query(
            """SELECT id, username, f_name, l_name, email, password FROM users
                WHERE username = \'%s\';""" % form.username.data)
        user_list = list(user)
        if user_list:
            if check_password_hash(user_list[0][5], form.password.data):
                user_obj = User(id=user_list[0][0], username=user_list[0][1], f_name=user_list [0][2], l_name=user_list [0][3],
                email=user_list[0][4], password=user_list[0][5])
                login_user(user_obj)
                return redirect('/profile')
            else:
                flash("Password is incorrect")
        else:
            flash("Account is not found")
    return render_template('homepage.html', form=form)


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='Page Not Found')


@app.errorhandler(500)
def majorError(error):
    return render_template('500.html', title='Major Error')
