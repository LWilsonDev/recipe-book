## Recipe Book Database Schema

### Collections:

#### Users 

	"_id": {
        "$oid": Mongo ObjectID
    },
    "username": String (same as "author" in recipes),
    "password": String (Hashed password)}

#### Recipes

    "_id": {
        "$oid": Mongo ObjectID
    },
    "title": String,
    "category": String,
    "author": String,
    "description": String,
    "ingredients": [],
    "vegetarian": String,
    "method": [] }


