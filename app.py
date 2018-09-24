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
    if 'username' in session:
        return "You are logged in as " + session['username']
    return render_template('index.html')

# Login and Signup inc password encryption code adapted from PrettyPrinted tutorial: https://github.com/PrettyPrinted/mongodb-user-login 
# https://www.youtube.com/watch?v=vVx1737auSE
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({"username" : request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), 
        login_user['password']) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return "Invalid username/password combination"
        
        
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





    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)    