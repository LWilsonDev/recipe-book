from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

app.config['MONGO_DBNAME'] = "recipe-book"
app.config['MONGO_URI'] = "mongodb://lwilsondev:lulue100@ds213053.mlab.com:13053/recipe-book"

mongo = PyMongo(app)


@app.route('/')
def index():

    return render_template('index.html', 
        breakfast_recipes=mongo.db.recipes.find({"category": "Breakfast"}),
        lunch_recipes=mongo.db.recipes.find({"category": "Lunch"}),
        dinner_recipes=mongo.db.recipes.find({"category": "Dinner"}),
        desert_recipes=mongo.db.recipes.find({"category": "Desert"}),
        vegetarian_recipes=mongo.db.recipes.find({"vegetarian": "Vegetarian"}),
        vegan_recipes=mongo.db.recipes.find({"vegetarian": "Vegan"}))

# Login and Signup inc password encryption code adapted from PrettyPrinted tutorial: https://github.com/PrettyPrinted/mongodb-user-login 
# https://www.youtube.com/watch?v=vVx1737auSE
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username']})
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
    
        return 'Invalid username/password combination'
    return render_template('login.html')    
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('index'))
        
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({"username": request.form['username'], "password": hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists!'
        
    return render_template('signup.html')

@app.route('/addrecipe', methods=['POST', 'GET'])
def addrecipe():
    
    if 'username' in session:
        if request.method == 'POST':
            
            ingredient = request.form['ingredients'].splitlines()
            method = request.form['method'].splitlines()
            recipes = mongo.db.recipes
            
            recipes.insert({"title": request.form['title'],
                            "category": request.form['category'],
                            "author": session['username'],
                            "description": request.form['description'],
                            "ingredients": ingredient,
                            "vegetarian": request.form['vegetarian'],
                            "method": method
                            })
            
           
            return render_template('addrecipe.html')
        
        return render_template("addrecipe.html")

    return "please login to add a recipe"        

@app.route('/recipe/<recipe_id>', methods=['POST', 'GET'])
def recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
   
    return render_template('recipe.html', recipe=the_recipe)

@app.route('/myrecipes/<username>/', methods=['POST', 'GET'])
def myrecipes(username):
    user_recipes = mongo.db.recipes.find({"author": username})

    return render_template('myrecipes.html', user_recipes=user_recipes,
                           username=username)


@app.route('/category/<category_name>', methods=['POST', 'GET'])
def category(category_name):
    if category_name == 'Vegetarian':
        the_category = mongo.db.recipes.find({"vegetarian": "Vegetarian"})
    elif category_name == 'Vegan':
        the_category = mongo.db.recipes.find({"vegan": "Vegan"})
    else:
        the_category = mongo.db.recipes.find({"category": category_name})
    return render_template('category.html', category_name=category_name, category=the_category)


@app.route('/edit_recipe/<recipe_id>', methods=['POST', 'GET'])
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = ["Breakfast", "Lunch", "Dinner", "Dessert"]
    vege_list = ["Not vegetarian", "Vegetarian", "Vegan"]
    
    return render_template("edit_recipe.html", recipe=the_recipe, categories=categories, vege_list=vege_list)

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    ingredient = request.form['ingredients'].splitlines()
    method = request.form['method'].splitlines()
    recipes.update({'_id': ObjectId(recipe_id)},
        {"title": request.form['title'],
                    "category": request.form['category'],
                    "author": session['username'],
                    "description": request.form['description'],
                    "ingredients": ingredient,
                    "vegetarian": request.form['vegetarian'],
                    "method": method
                    })
    return redirect(url_for('recipe', recipe_id=recipe_id))
    
@app.route('/delete_recipe/<recipe_id>', methods=["GET"])
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('myrecipes', username=session['username']))   
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)    