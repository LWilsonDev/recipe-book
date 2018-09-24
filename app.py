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
@app.route('/login')
def login():
    return render_template("login.html")





    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)    