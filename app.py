from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import os
import config


app = Flask(__name__)


####### Config Vars ######

# set development and testing to False for deployment
development = True

if development == True:
    app.config.from_object('config.DevelopmentConfig')

else: 
    # environment variables set in Heroku config for deployed sit
    app.secret_key = os.environ['SECRET_KEY']
    app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']
    app.config['MONGO_URI'] = os.environ['MONGO_URI']
    DEBUG=False
        
######### 


mongo = PyMongo(app)    

@app.route('/')
def index():
    '''
    Render home page
    '''
    return render_template('index.html')


# Login and Signup inc password encryption code adapted from PrettyPrinted tutorial: 
#https://github.com/PrettyPrinted/mongodb-user-login 

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    If request method is POST, function finds username from database and compares encrypted passwords.
    If they match the user is logged in.
    
    """
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                flash('Welcome back, ' + session['username'])
                return redirect(url_for('index'))
        flash('Invalid username/password')        
    return render_template('index.html')
    
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out')
    return redirect(url_for('index'))
    
        
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    If username is unique, password is encrypted and user is added to database. 
    User is then logged in (username in session).
    """
    
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({"username": request.form['username'], "password": hashpass})
            session['username'] = request.form['username']
            flash("Welcome, " + session['username'])
            return redirect(url_for('index'))
            
        flash('That username already exists!')
    return redirect(url_for('index'))
    
        
@app.route('/addrecipe', methods=['POST', 'GET'])
def addrecipe():
    '''
    A logged-in user can add a new recipe to the db
    '''
    if 'username' in session:
        if request.method == 'POST':
            
            ingredient = request.form['ingredients'].splitlines()
            recipes = mongo.db.recipes
            
            recipes.insert({"title": request.form['title'],
                            "category": request.form['category'],
                            "author": session['username'],
                            "description": request.form['description'],
                            "ingredients": ingredient,
                            "method": request.form['method'],
                            "vegetarian": request.form['vegetarian']
                            })
            
            return redirect(url_for("myrecipes", username=session['username']))
        
        return render_template("addrecipe.html")
    #If user navigates to /addrecipe but isnt logged in, show error    
    flash("Please login to add a recipe")
    return render_template("index.html") 
    

@app.route('/recipe/<recipe_id>', methods=['POST', 'GET'])
def recipe(recipe_id):
    '''
    Detail page for each recipe
    '''
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=the_recipe)


@app.route('/myrecipes/<username>/', methods=['POST', 'GET'])
def myrecipes(username):
    '''
    Shows all recipes of the user, or all recipes from one specific author
    '''
    user_recipes = mongo.db.recipes.find({"author": username})    
    return render_template('myrecipes.html', user_recipes=user_recipes,
                           username=username)


@app.route('/category/<category_name>', methods=['POST', 'GET'])
def category(category_name):
    '''
    Shows list of all recipes in a category
    '''
    if category_name == 'Vegetarian':
        the_category = mongo.db.recipes.find({"vegetarian": "Vegetarian"})
    elif category_name == 'Vegan':
        the_category = mongo.db.recipes.find({"vegetarian": "Vegan"})
    else:
        the_category = mongo.db.recipes.find({"category": category_name})
    return render_template('category.html', category_name=category_name, category=the_category)


@app.route('/edit_recipe/<recipe_id>', methods=['POST', 'GET'])
def edit_recipe(recipe_id):
    '''
    Page for editing a recipe
    '''
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = ["Breakfast", "Lunch", "Dinner", "Dessert"]
    vege_list = ["Not vegetarian", "Vegetarian", "Vegan"]
    return render_template("edit_recipe.html", recipe=the_recipe, categories=categories, vege_list=vege_list)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    '''
    Updates the editted recipe on the db
    '''
    recipes = mongo.db.recipes
    ingredient = request.form['ingredients'].splitlines()
    method = request.form['method'].splitlines()
    recipes.update({'_id': ObjectId(recipe_id)},
        {"title": request.form['title'],
                    "category": request.form['category'],
                    "author": session['username'],
                    "description": request.form['description'],
                    "ingredients": ingredient,
                    "method": method,
                    "vegetarian": request.form['vegetarian']
                    })
    return redirect(url_for('recipe', recipe_id=recipe_id))
 
    
@app.route('/delete_recipe/<recipe_id>', methods=["GET"])
def delete_recipe(recipe_id):
    '''
    deletes recipe from the db
    '''
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('myrecipes', username=session['username']))   
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')))    