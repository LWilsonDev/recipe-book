from flask import Flask, render_template, url_for, request, session, redirect
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
    #if 'username' in session:
        #return "You are logged in as " + session['username']
    return render_template('index.html', 
    breakfast_recipes=mongo.db.recipes.find({"category": "Breakfast"}),
    lunch_recipes=mongo.db.recipes.find({"category": "Lunch"}))

# Login and Signup inc password encryption code adapted from PrettyPrinted tutorial: https://github.com/PrettyPrinted/mongodb-user-login 
# https://www.youtube.com/watch?v=vVx1737auSE
@app.route('/login', methods=['GET', 'POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})
    if request.method == 'POST':
        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
    
        return 'Invalid username/password combination'
    return render_template('login')    
        
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({"username": request.form['username']})
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({"username": request.form['username'],"email": request.form['email'], "password" : hashpass })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username already exists!'
        
    return render_template('signup.html')

@app.route('/addrecipe', methods=['POST', 'GET'])
def addrecipe():
    
    if 'username' in session:
        if request.method == 'POST':
            ingredient_list = []
            for quantity, ingredient in zip(request.form.getlist('quantity'),
                                          request.form.getlist('ingredient')):
                result = (quantity, ingredient)
                ingredient_list.append(result)
                
               
            ingredient_dict = dict(ingredient_list)
            print(ingredient_list)
            print(ingredient_dict)
            recipes = mongo.db.recipes
            
            recipes.insert({"title": request.form['title'],
                            "category": request.form['category'],
                            "author": session['username'],
                            "description": request.form['description'],
                            "ingredients": ingredient_dict,
                            "vegetarian": request.form['vegetarian']
            })
            
            
            return render_template('index.html')
        
        return render_template("addrecipe.html")

    return "please login to add a recipe"        

@app.route('/recipe/<recipe_id>', methods=['POST', 'GET'])
def recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
   
    return render_template('recipe.html', recipe=the_recipe)

    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)    