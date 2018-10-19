# Vanlife Recipes

This is an online campervan cookbook, providing a place for campervan enthusiasts and vanlifers to find and store recipes suitable for life on the road.

This web app is built using Python, Flask, and utilises MongoDB. Users can view all recipes by category (and by author), and they can register and login to add their own recipes. 

**View the app [here](http://vanlife-recipes.herokuapp.com/)**

**View files [here](https://github.com/LWilsonDev/recipe-book)**


# UX

I aimed to keep the layout simple and uncluttered, with a minimum-fuss approach to the login/register to improve UX. 

#### User stories:

- I want to browse the recipes without having to sign up. 
- If I find a recipe I like, I can see other recipes by the same author.
- I want to be able to sign up to add my own recipes to share with the community
-  I should be able to view/edit/delete my recipes.
- I am a vegetarian/vegan and only want to view recipes suitable for me.


## Features

#### Homepage:

-  If the user is not logged in they will find buttons offering login/register.
- Login/register are simple pop-out modals, meaning the user does not have to navigate to a separate page to login.
- Once logged in, the user has the option to add a new recipe or view their recipes.
- The user is shown an error message or a success message after login.
- 6 Recipe categories are displayed with pictures that can be clicked - taking the user to a new page with all the recipes in that category.

#### Recipes:

- All recipes are links to the detailed page of that recipe.
-  Each recipe page includes the ingredients, method, and a link to the authors' other recipes.
- If the user is the author of that recipe, they will see "edit" and "delete" buttons.

#### Add Recipe:

- A logged in user can add a recipe to the database using a clear and simple to use form. 
- The form has some validation and error messages using javascript to alert the user if they have not provided a category or vegetarian information. 

#### Edit Recipe:
- The author of the recipe can edit and delete the recipe. The existing information is preloaded into the form.

### Features Left to Implement

-   Likes/recipe ratings
-  Comments
- Search by ingredient

## Technologies Used

-   [Python](https://python.org/): The backend of this project is written in python
-    [Flask](http://flask.pocoo.org/): This lightweight framework was used to create the app. It has many useful features including 'session' and 'PyMongo' as well as Jinja 2 templating for interacting with the frontend.
- [Materialize.css](http://archives.materializecss.com/0.100.2/): I used this Materialize.css version 0.100.2 to speed up development and keep the design consistent throughout the app. I liked its simplicity and thought the nav elements and responsive grid system was easy to use. The modal pop-outs were very simple and effective.
  
-   [JQuery](https://jquery.com/): Materialize.css version 0.100.2 uses JQuery, and I also used it to set up alerts for the form validation. It can be found on the base.html file.
-  [MongoDB](https://mongodb.com/): I used this non-relational database for this app. I used [mLab](https://mlab.com/) to access the database easily. I chose to have 2 collections, 'Users' and 'Recipes'. The two collections are connected by a shared value - the Author/Username. My schema can be found [here](https://github.com/LWilsonDev/recipe-book/blob/master/database/database-schema.md)


## Testing

I did not automate tests for this project, however in future I would choose to write automated tests to test the CRUD aspects of the app/database.

I underwent thorough manual testing of each element.  

[mLab](https://mlab.com/) was particularly useful for developing the CRUD features as I was able to easily see what data was being sent to the database.

#### Screen sizes:

The layout was designed using a "mobile first" approach, with  changes at the medium and large breakpoints. 

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

#### Bugs:

- There were some issues with the 'add recipe' form submitting correctly. If the user had not selected a category or vegetarian option then the form would not submit. Adding a 'required' html tag did not fix the bug. Instead, I had to use Javascript/Jquery to check if the options were selected when the "add recipe" button was clicked - and alert the user if not.
- When there was not much content on a page, the footer did not display at the bottom of the page. Using CSS to position it did not have the desired results for all the pages, instead I gave the <main> section a minimum height.

#### Bugs left to fix:

- If the user does not have any recipes currently the 'card' is still visible. Instead, I would like to check the database and if there are no recipes for that user, there should be a message saying "You don't have any recipes yet." 
- When the user wants to edit the recipe, the form fields should be filled in. However, the dropdown options do not always have the value selected, and even if they do, the javascript asking the user to select an option still runs.


## Deployment

The project is deployed on Heroku. I followed these steps:

- Initialise git repository
- Create requirements.txt and a Procfile 
- Login to Heroku and create the app, follow instructions for setting up remote git repo.
- Push the git repository to Heroku
- Select dyno
- Set Config Vars to IP 0.0.0.0 and PORT 5000

To run the files locally, download the files from the github repo, ensure all requirements are installed.

## Credits

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

#### Acknowledgements

- Login and Signup  password encryption code adapted from PrettyPrinted tutorial: https://github.com/PrettyPrinted/mongodb-user-login 
https://www.youtube.com/watch?v=vVx1737auSE