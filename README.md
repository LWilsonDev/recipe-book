# Vanlife Recipes

### Vanlife: living full-time in a (often self-built) campervan.

This is an online campervan cookbook, providing a place for campervan enthusiasts and vanlifers to find and store recipes suitable for life on the road with small/limited cooking facilities.

This web app is built using Python, Flask, and utilises MongoDB. Users can view all recipes by category (and by author), and they can register and login to add their own recipes. 

**View the app [here](http://vanlife-recipes.herokuapp.com/)**

**View files [here](https://github.com/LWilsonDev/recipe-book)**


# UX

I aimed to keep the layout simple and uncluttered, with a minimum-fuss approach to the login/register to improve UX.

The colour-scheme is fun and bright, with bright orange heading text. This is to reflect the retro/alternative 'style' associated with vanlife.

I used a similar layout across the site's pages to aid UX and keep a consistent style. The images on the 'category' and 'author/my recipes' pages are of different camper vans. There is a collection of 10 different images which are randomly selected each time the page loads. This was to keep the theme of 'vanlife' and add interest to the pages.

#### User stories:

- I want to browse the recipes without having to sign up. 
- If I find a recipe I like, I can see other recipes by the same author.
- I want to be able to sign up to add my own recipes to share with the community
- I should be able to view/edit/delete my recipes.
- I am a vegetarian/vegan and only want to view recipes suitable for me.


## Features

#### Homepage:

- If the user is not logged in they will find buttons offering login/register.
- Login/register are simple pop-out modals, meaning the user does not have to navigate to a separate page to login.
- Once logged in, the user has the option to add a new recipe or view their recipes.
- The user is shown an error message or a success message after login.
- 6 Recipe categories are displayed with pictures that can be clicked - taking the user to a new page with all the recipes in that category.

#### Recipes:

- All recipes are links to the detailed page of that recipe.
- Each recipe page includes the ingredients, method, and a link to the authors' other recipes.
- If the user is the author of that recipe, they will see "edit" and "delete" buttons.

#### Add Recipe:

- A logged in user can add a recipe to the database using a clear and simple to use form. 
- The form has some validation and error messages using javascript to alert the user if they have not provided a category or vegetarian information. 

#### Edit Recipe:
- The author of the recipe can edit and delete the recipe. The existing information is preloaded into the form.

### Features Left to Implement

- Likes/recipe ratings
- Comments
- Search by ingredient

## Technologies Used

- [Python](https://python.org/): The backend of this project is written in python
- [Flask](http://flask.pocoo.org/): This lightweight framework was used to create the app. It has many useful features including 'session' and 'PyMongo' as well as Jinja 2 templating for interacting with the frontend.
- [Materialize.css](http://archives.materializecss.com/0.100.2/): I used this Materialize.css version 0.100.2 to speed up development and keep the design consistent throughout the app. I liked its simplicity and thought the nav elements and responsive grid system was easy to use. The modal pop-outs were very simple and effective.
- [JQuery](https://jquery.com/): Materialize.css version 0.100.2 uses JQuery, and I also used it to set up alerts for the form validation. It can be found on the base.html file.
- [MongoDB](https://mongodb.com/): I used this non-relational database for this app. I used [mLab](https://mlab.com/) to access the database easily. I chose to have 2 collections, 'Users' and 'Recipes'. The two collections are connected by a shared value - the Author/Username. My schema can be found [here](https://github.com/LWilsonDev/recipe-book/blob/master/database/database-schema.md)


## Testing

Unit tests for the login/register/logout functionality can be found [here](https://github.com/LWilsonDev/recipe-book/blob/master/test.py)
These tests can be ran from the command line using "python3 test.py" 

The automatic tests check the following: 

#### Login:
- Returning users with correct password should see a "welcome back" message
- Unregistered or returning users with incorrect password should see "invalid login/password"

#### Register:
- Users with an existing username should see "that username already exists"
- New users entering a unique username and password should be logged in and see "logged in" message

#### Logout:
- Users should be redirected to index page and see "logged out" message.


I underwent thorough manual testing of each element including:

- Once logged in, users can add a recipe to the database. The recipe should have a title of no more than 40 letters, and must not include special characters other than '&' and punctuation.
- If the user does not select a category or vegetarian/not, or if they do not give the recipe a title they will see an error message. The title error message is the browser "required field" error, the vege/catagory selection error is powered by javascript and should read either: 'Please select a category for your recipe' or "Please select an option to indicate if your recipe is suitable for vegetarians" depending on which selection is missing.
-  Users will not be able to add recipes once logged out.
-  All links work
-  Users cannot reach the add recipe page unless they are logged in. The will see an error "Please login to add a recipe" and be redirected to the home page
-  The website was tested across different screen sizes and devices to ensure elements were displayed correctly

[mLab](https://mlab.com/) was particularly useful for developing the CRUD features as I was able to easily see what data was being sent to the database.

#### Screen sizes:

The layout was designed using a "mobile first" approach, with  changes at the medium and large breakpoints. 

On small screens, each recipe category takes up the full width of the screen, as does the header with login buttons.
On medium screens, the recipe categories are in rows of 2 and the header takes up 2/3.
On large screens, the recipe categories are in rows of 3 and the header and image share half the screen.

The navbar is a side-nav with burger-icon for small and medium screens, and is a full top-navbar with dropdown links for larger screens.

#### Bugs:

- There were some issues with the 'add recipe' form submitting correctly. If the user had not selected a category or vegetarian option then the form would not submit. Adding a 'required' html tag did not fix the bug. Instead, I had to use Javascript/Jquery to check if the options were selected when the "add recipe" button was clicked - and alert the user if not.
- When there was not much content on a page, the footer did not display at the bottom of the page. Using CSS to position it did not have the desired results for all the pages, instead I gave the <main> section a minimum height.

#### Bugs left to fix:
- Security issues around forms. I need implement better security features to protect against cross-site scripting. At the moment, special characters cannot be entered into the text input due to the regex pattern specification, but ideally I will implemet CSRF tokens using Flask WTForms to better protect form inputs in future.
- When the user wants to edit the recipe, the form fields should be filled in. However, the dropdown options do not always have the value selected, and even if they do, the javascript asking the user to select an option still runs.


## Deployment

The project is deployed on Heroku. I followed these steps:
```
heroku login
heroku apps create recipe-book
```
- Create requirements.txt and a Procfile
```
git push -u heroku master
heroku ps:scale web=1
```
- Set Heroku app settings - Config Vars to IP 0.0.0.0 and PORT 5000
- I had mistakenly included other config vars to git repo so I needed to change them and make them environment variables before deployment.
- I changed the app 'secret_key' and database information including passwords, and made them new environment variables.
- I then set these variables in Heroku app settings - Config Vars.

### Development/deployment:
The config vars are different for devlopment and deployment. For development, set "development = True" in app.py. Config vars will need to be set in a config.py file as follows:
```
import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = <your_secret_key>
    MONGO_URI = <your_mongo_uri>
    MONGO_DBNAME = <your_db_name>
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    
```

### To run the files locally:

- Download the files from the github repo, ensure all requirements are installed and environment variables are set ups:
```
pip install -r requirements.txt
python3 app.python
```

## Credits

This app is intended only as an educational project, not for actual real-world deployment.

#### Content:

-   The recipes are from http://www.sprintervandiaries.com/2015/07/02/vanlife-cookbook/

#### Photos:

https://unsplash.com/photos/HzVHlwvQlyw by nickldn 
https://unsplash.com/photos/r-dChNeNKk8 by kevin mccutcheon 
https://unsplash.com/photos/9Er-MNdzrPA by jen kosar 
https://unsplash.com/photos/9aUU5PGZfxY by Toa Heftiba 
https://unsplash.com/photos/zOlQ7lF-3vs by jennifer schmidt
https://www.vegansociety.com/whats-new/blog/vegan-road-victorias-creative-kitchen
https://unsplash.com/photos/N16iTD8g2s0 By Natural Chef Carolyn Nicholas 
https://unsplash.com/photos/Mta8r0bxhbo by Kevin Schmid
https://unsplash.com/photos/GTDoOSzbDnk by Fabien Rousselot
https://unsplash.com/photos/DAkJbq-15EI by Lucas Favre
https://unsplash.com/photos/GUWdkUjYlKA by Danny Halarewich
https://unsplash.com/photos/0Epkj3JItao by Alice Hartrick
https://unsplash.com/photos/d5FMKCK0J3I by Brina Blum
https://unsplash.com/photos/yL5Vp57D6U4 by Livin4Wheel
https://unsplash.com/photos/Af1OMQpuN14 by Ian Usher

#### Acknowledgements

- Login and Signup  password encryption code adapted from PrettyPrinted tutorial: https://github.com/PrettyPrinted/mongodb-user-login 
- JQuery pagination plugin https://www.jqueryscript.net/table/jQuery-Table-Pagination-For-Materialize.html