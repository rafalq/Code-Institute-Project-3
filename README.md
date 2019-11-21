# Project 3 - Online Cookbook

Code Institute - Data Centric Development Milestone Project

Rafal Kruszewski 

Project Idea:  An Online Cookbook

This is my online cookbook website which is the third Milestone Project in the Fullstack Web Developer course.

I am myself a keen cook, that is why I picked the idea for the project. I usually use the internet when I want to revise a recipe or I look for some inspiration for my weekend dinner.

## UX

### User Stories

User 1 looks for a recipe for a specific meal(cuisine, type, people opinions).
User 2 has added their recipe and wants to update it or delete it.
User 3 wants to add their recipe.
User 4 had a delicious lunch and wants to give the thumbs up to the recipe.

### Strategy

My goal was to create an online version of a cookbook that could be easy to use especially to move around. I added only necessary options according to the project idea requirements.

### Scope

(User 1) I placed the statistical table on the home webpage to enable the user to find her/his recipe by a cuisine, a meal type or a review score.

(User 2) I wanted to provide an easy way to update a recipe by changing the input text and confirming it with the Update button. The recipe can be deleted on the same webpage by using the `Delete` button.

(User 3) I placed a link `Share Your Recipe` on the navigation bar which gets the user to a webpage where they can add their recipe by fullfiling a form.

(User 4) I gave users a possibility to review any recipe by rating it in the rate section in the recipe page.

### Structure

The website consists of 9 pages:

**base.html** and **base_for_form.html**

These webpages are inherited by the rest pages. Both of them have the title and a navigation bar which includes a search field, an  `Share Your Recipe` link.

The `base.html` contains additionaly a badge with the amount of all recipes and a statistical table where you can find three categories: Cuisine, Meal Type, Ratings.

**home.html**

This is a main webpage inherits base.html. It contains all added recipes that are displayed in three columns.

**recipes.html, reviewed_recipes.html, vegetarian_recipes.html**

These are webages where users are directed to when they clicked any field in the statistical table. They display the recipes belong to the relevant category.

**edit_recipe.html**

The website is an actual recipe description. It contains the navigation bar at the top and a few sections below. First - an image with a rating score and a short recipe description. Next to it we can find the recipe title, the author, a meal type, the kind of cuisine, a hot or vegetarian sign icons, a number of servings, cook and preparation time.

There is `Rate the recipe` section lower. We find `Ingredients` next to an example of an advertisment. At the very bottom, there is `Method` section.

**update_recipe.html**

When an user clicks one of these: the title, the author, the image, the `Ingredients` or the `Method` header, they are directed to the `update_recipe` webpage which is a form including the fullfilled recipe fields, that can be modified. There is a advertisment section in the middle of the page. At the very bottom, we can find two buttons: the green one updates the recipe and the grey one - delete it.

**share_your_recipe.html**

Users can get there by clicking `Share Your Recipe` link in the navigation bar.
The webpage is a blank form contains titled input fields, the default image and the `Submit` button.

 
### Skeleton

[home.html wireframe](https://github.com/rafalq/Code-Institute-Project-3/blob/master/wireframes/home.jpg/home.jpg)

[recipes.html wireframe](https://github.com/rafalq/Code-Institute-Project-3/blob/master/wireframes/recipes.jpg)

[edit_recipe.html wireframe](https://github.com/rafalq/Code-Institute-Project-3/blob/master/wireframes/edit_recipe.jpg)

[share_your_recipe.html wireframe](https://github.com/rafalq/Code-Institute-Project-3/blob/master/wireframes/share_your_recipe.jpg)

[update_recipe.html wireframe](https://github.com/rafalq/Code-Institute-Project-3/blob/master/wireframes/update_recipe.jpg)

### Colors

Main colors are: blue, grey, red and blend of those three. They seem to harmonize and complement each other. To keep the color consistency, the materialize css style was overrided.

## Technologies

1. Flask Microframework (1.1.1)
2. Javascript
3. MongoDB (4.2)
4. Materialize (1.0.0)
5. HTML5
6. CSS3

## Features

### 1. The Home Page
#### (home.html)

Starting from the top of the page,

Each of the has the app title. It is an actual anchor element which after being clicked takes the user to the home page. 

You can see the search field in the navigation bar section where any word can be entered to find your recipe.

The code I used creates a wildcard index on all fields so that way any word can be found in the value of the document

```
	search_title = request.form.get('search_name')
	mongo.db.recipes.create_index([('$**', 'text')])
		recipes = mongo.db.recipes.find({'$text': {'$search': search_title}})
```

Next to the
**Go**
button which starts searching, there is  the

**Share Your Recipe**
link, which takes the user to a blank recipe form, and a red badge - with the number of all available recipes. 

A little below, they can find

the **Statistics Table**
that includes three category:
- Cuisine,
- Meal Type,
- Ranking.

```
	count_cuisines = mongo.db.recipes.aggregate([ {'$group': { '_id':
```

The code above counts the documents with the same key and the value.

It is used for the cuisine and the meal type.

* The Cuisine displays the number of recipes for each kind.

* The Meal Type does the same for each kind of meal.

For counting each rating score I used this :

```
	for recipe in mongo.db.recipes.find({ "score": { "$exists": True } }):
        if (recipe["score"] // recipe["votes"]) == 5:
            five_counter += 1
        elif (recipe["score"] // recipe["votes"]) == 4:
            four_counter += 1
        elif (recipe["score"] // recipe["votes"]) == 3:
            three_counter += 1  
        elif (recipe["score"] // recipe["votes"]) == 2:
            two_counter += 1
        lif (recipe["score"] // recipe["votes"]) == 1:
            one_counter += 1
```

For unreviewed recipes, a similar code was used. This time it checks if there is no votes for the recipe

```
	for recipe in mongo.db.recipes.find({'votes': {'$exists' : False} }):
        no_review_counter += 1
```
 
* The Ranking is divided into six fields from five navy stars to one and the white star, which is for the recipes without any rating score.

By clicking any of the fields described above, the user is taken to the relevant webpage containing recipes for the chosen field.   

The table is an accordion materialize element which is active when you reach the page. Each of the category header has a arrow button that hide the content when is pressed.

the **Card**

Every recipe on this page is diplayed in a card form that has an image at the top, the title, a "Read me..." link, a three vertical aligned dots icon.

When you click the icon, you are taken to the other side of the card where you can find the rating score, a short description of the dish and vegetarian, hot meal icons (if they are asigned to the recipe).

When the "Read me" link is clicked, the user is taken to the page (edit_recipe.html) which displays all information about the recipe.


### 2. The Found Recipes Pages 
#### (recipes.html, reviewed_recipes.html, vegetarian_recipes.html)

These webpages displays the relevant recipes in the card form. These cards are desingned in the same way as those above.

At the top there is the name of the app which takes to the homepage when it is clicked.

The navigation bar has the same elements as the homepage navbar excluding the badge.
The amount of the found recipes is displayed in the paragraph just below.

I used the `<p>` element and javascript to display the number. Javascript sums up the amount of card titles.

```javascript
	var found = document.getElementsByClassName("found-title");
	var foundAmount = found.length;
```

### 3. The Recipe Page
#### (edit_recipe.html)

The page consists of five sections.

**The app title and the navbar**

These elements are the same as those above.

**Top section**

*Image is linked by the `<a>` element to the update page.
 
*The Rating score is displayed by star icons where one is the lowest score and five is the maximum the recipe can receive and the number of votes. 

I used a `for` loop in flask for this. Because votes are summed up in the database, to find the score for the recipe I needed the average of the score and the votes, thus:

```
	{% for x in range(recipe.score // recipe.votes) %}
		<i id="edit-card-star" class="material-icons">star</i>
	{% endfor %}
```

The short description is placed below the image.

The recipe title and the autor can be clicked to access the update page.

The meal type, the cuisine, the servings, the preparation and the cooking time are displayed along with the name and the relevant icon.

**Rate the Recipe** section

To unclock the section, the user need to click one of the star icon that represents the rating from one to five. The vote button sends the score to the database.

I used javascript for this.

* unblock the button
```javascript

	var firstStar = document.getElementById("star-1");
	function firstStarClick(){
		button.removeAttribute("disabled");
	}
```

* pick the rating
```javascript
	function firstStarClick(){
		vote.setAttribute("value", 1);
	}
```
* change the star colors for the relevant score
```javascript
	function secondStarClick(){
		this.style.color="red";
		firstStar.style.color="red";
		thirdStar.style.color="pink";
		fourthStar.style.color="pink";
		fifthStar.style.color="pink";
	}
```
* to block the button, the user needs to click the first star icon twice.
```javascript
	if((this.style.color=="red") && (this.nextElementSibling.style.color=="pink")){
		this.style.color="pink";
		vote.setAttribute("value", 0);
		button.setAttribute("disabled","");
		textColor.style.color="gray";
	}
```

After clicking the Vote button, we are taken to the home page where we can see the message on the green 

** Middle section **

* The ingredients are diplayed the same way as they were typed, keeping the original indentation and spaces. To do this I used the `<textarea disabled>`. The header is connected with the update page by `<a>`.

* The example of advertisment is designed to differentiate from the other content. I used a different color for the header and a different `<font-famiy>` for the text.

**Bottom section**

The `Method` as the `Ingredients` section uses the same element to be recreated in the same way. The header is connected with the update page.


### The Form Page 
#### (share_your_recipe.html)

After clicking the `Share Your Recipe` on the navbar, the user is taken to a webpage which is a blank form.

There are twelve fields there.

For the Ingredients , the `Short Description` and the `Method` I used a `materialize-textarea` class to enable users to type their text in a new line.

For one sentence field I used materialize `input`.

The meal type is a materialize `collapsible` element, that has hidden `anchors` elements with names of meals.

The vegetarian and hot checkboxes are desiged using a materialize `<input type="checkbox">` so that their values in the database are `on` or `null`.

When any field is clicked, the icon, the title and the bottom border changed its color for navy. 

1. Recipe Title (input)
2. Meal Type (collapsible)
3. Image (input) with a button 
4. Cuisine (input)
5. Vegetarian checkbox (input)
6. Hot checkbox (input)
7. Prep (input)
8. Cook (input)
9. Ingredients (textarea)
10. Short Description (textarea)
11. Method (textarea)
12. Author (input) with the Submit button.

When the user clicks the `Submit` button, the form is sent to the database

```
	recipes.insert_one(request.form.to_dict())
```

and they are redirected to the home page.

The flask "flash" message is displayed just below the navigation bar to confirm the operation.

### 4. The Update/Delete Page (update_recipe.html)

When the user hovers over the image of the recipe, the recipe title, the author, the Ingredients heading or the Method heading on the edit_recipe page, the tooltipped information says `Update/Delete Recipe`.

After clicking one of these above, they are directed to the update page, which is a form the same as the `share_your_recipe` page. The text in the input fields is recreated in the same order as it was typed.

There is a little difference between this form and the previous one. This time the author field is at the top of the page, the middle area contains an ad section and there are two buttons at the bottom.

When the user clicks any of the fields with an icon, they can make any changes to the text.

The meal type can be changed for another one.

The vagetarian and the hot checkboxes can be checked or unchecked.

All of the field are required. The form can not be sent to the database with any empty field.

As the user clickes the submit button, they are take to the homepage and get the message confirming that the recipe has been updated.
The code for this uses:

```
	recipe.update({'_id': ObjectId(recipe_id)},{
        '$set':{
            'recipe_title':request.form.get('recipe_title'),
            'author':request.form.get('author'),
            'cuisine':request.form.get('cuisine'),
            'prep_time':request.form.get('prep_time'),
            'cook_time':request.form.get('cook_time'),
            'servings':request.form.get('servings'),
            'ingredients':request.form.get('ingredients'),
            'short':request.form.get('short'),
            'description':request.form.get('description'),
            'vegetarian':request.form.get('vegetarian'),
            'hot':request.form.get('hot'),
            'meal_type':request.form.get('meal_type'),
            'image':request.form.get('image')
        }
        })
``` 

There is a black button at the bottom of the page that delete the recipe.
 
### Features Left to Implement

First of all a sign-in and login option is neccesary for this kind of website where you can vote or manipulate data from the website. That was beyond of the project scope.

Pagination for the `homepage`. In time the cookbook will have more and more recipes. Some limitation for displaying a number of them for example showing just the latest thirty would be a good idea. That would prevent from slowing down to load and simultaneously update the content of the page.

An original logo designed exclusively for the website.

An option for uploading ones recipe image. I am completely new to the database topic and as I understand reading some posts on the stockoverflow website, adding media files to mongodb is not recommended.
However good pictures improve the UX greatly so I think this option is important. I tried to implement this partialy providing some images to test the recipes design with and without a picture.

A blog for users containing ideas, suggestions for the recipes.

## Testing

### Frontend

 __HTML__
 
 [W3C Markup Validation]( https://validator.w3.org/) was used to validate HTML.

__base.html__

> Error: The element input must not appear as a descendant of the button element.

> From line 62, column 8; to line 62, column 122

I needed to place these elements in this way for two purposes. I wanted everyone of the cuisine names to be able to be clicked, what was impossible if the element had not been nested inside the `<button>`. For the backend I needed an `<input>` element with the `<value>` attribute so that could be `<readonly>` and could be sent to the database as the request value.
Everything worked perfectly so I did not have any reason to change the above.

 __CSS__
 
 [W3C CSS validation](https://jigsaw.w3.org/css-validator/) was used to validate CSS.

The rest tests were run manually.

 __Javascript__

__base.html__, __base_for_form.html__, __edit_recipe.html__

	Hover the cursor over the logo, the Share Your Recipe word.
	Type a text into the search field and press the Go button.
	Check the badge number displays correct amount of recipes.
	Click the Share Your Recipe word. 
	
__home.html__

	Click the recipe title on the card.
	Click the three dot icon on the card.
	Click the "Read more..."

__edit_recipe.html__

	Hover the cursor over the image, the recipe title, the author, the Ingredients name, the Method name.
	Click the Logo.
	Check if the Vote button is disabled by clicking it.
	Click each of the star icon.
	Click the first icon from the left twice.
	Click the Vote button when it is disabled.
	Click one of the icons again.
	Click the button when it is red color.

__recipes.html__, __reviewed_recipes.html__, __vegetarian_recipes.html__

	Click the Logo.
	Check if the number for the message is correct by comparing it with the number from the statistical table.
	Check if the message is "Found 1 recipe" if there is found only one recipe, refer to the table from the homepage.
	Check if the message is "Sorry, no matches" if there is no recipe (zero) for the clicked name from the table.

__share_your_recipe.html__, __update.html__

	Click the arrow icon from the Meal Type field.
	Click each appeared word.
	Click the icon again.

### Backend

#### Python, flask, mongodb  

All tests for the backend were run manually.

__base.html__, __base_for_form.html__, __edit_recipe.html__

	Type some text into the search bar and click the Go button.

__home.html__

	Type a text that into the search field and press the Go button.
	Check if everyone of the cuisine number is correct by comparing it with the relevant key in the database and sums up all with same value.
	Check if the vegeterian cuisine number is correct by comparing it with the relevant key in the database, adds all the vegeterian key with the value "on".
	Check if everyone of the meal type number is correct by comparing it with the relevant key in the database and sums up all with same value.
	Check if everyone of the rating number is correct by comparing it with the relevant key in the database, divide the score value by the votes.
	Click each name from the statistical table.
	Check if the other side of the card displays correct recipe details(the rating, the vegeterian icon, the hot icon, the short description).

__recipe.html__, __reviewed_recipes.html__, __vegetarian.html__

	Type a text that will be found into the search field and press the Go button.
	Check if there is the correct amount of found recipes.

__edit_recipe.html__

	Type a text that will be found into the search field and press the Go button.
	Check if all recipe details are correct and corresponding with the relevant keys and values from the database.
	Click one of the star from the rating section and press the Vote button. Check if the score and the votes of the recipe were updated in the database and in the statistical table.
	
__share_your_recipe.html__, __update_recipe.html__

	Type a text that will be found into the search field and press the Go button.
	Fullfill each input field and clear one of them, check if you do not manage to send the form and receive the message "Please fill out this field". Repeat the test for each of the fields.
	Fullfill the form and click the Submit button.
	
### IMPORTANT!
	
> For a design purpose, I created an option for uploading images as I explained above.
> All images used for the recipes are kept in this [folder](https://github.com/rafalq/Code-Institute-Project-3/blob/master/static/images)
> Please use one of the images providing in the folder by entering the exact name with the extension into the field.
> If you do not do this, there is one set as default.

	Click the Vegetarian and the Hot checkboxes and press the Submit button.

__update_recipe.html__

	Click the Delete button.
	
The website can be open with the browsers:  `Firefox (Version 70.0.1`), `Opera (Version 63.0.3)`, `Internet Explorer (Version 11.0.9)`, `Google Chrome (Version 77.0.3 `); responsive on mobiles, tablets, kindels.

I had some issues with The Google Chrome Dev Tools when I tested the website on different media screens. There was something wrong with zooming or additional white space was added for mobiles screen.

I found some tips on the Stack Overflow that this could have something to do with the materialize autoresizing. First I added this code to prevent from that but the same time that prevents users from resizing documents:

```
 <meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width, height=device-height, target-densitydpi=device-dpi">
```
then I removed the code and I checked the website on the Firefox Web Developer, a few mobiles, a tablet and a laptop using heroku url and everything looked perfect.

I also needed to add a scroll bar and to set the height for the ingredients and the method textareas otherwise the text inside that did not fit into the fields was cut off.

## Deployment

### Locally

You will need:
- An IDE (i.e Eclipse, Notepad, Sublime text, Atom)
- [Python 3](https://www.python.org/downloads/)
- Install [PIP](https://pip.pypa.io/en/stable/installing/)
- Install [Git](https://www.atlassian.com/git/tutorials/install-git#:~:targetText=Install%20Git%20on%20Windows,-Git%20for%20Windows&targetText=Download%20the%20latest%20Git%20for%20Windows%20installer.,pretty%20sensible%20for%20most%20users.) 
- Install [MongoDB](https://www.mongodb.com/download-center)

1. Use [this](https://github.com/rafalq/Code-Institute-Project-3.git) to conect to my github account.

2. Click the button "Clone or download" and choose "Download ZIP" option. If you have git installed, you can just type the code below in your command prompt:

```
git clone https://github.com/rafalq/Code-Institute-Project-3.git
```

3. Install all required modules with the command:
 
```
pip -r requirements.txt.
```

4. Create the secret key as an environmental variable in your system. Refer to this code:

```
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
```

or do assign it to this expression

```
app.config["SECRET_KEY"] = <your secret key here>
```

5. Log into your database. Create a new database and call it `online-cookbook`.

6. Create a collection for the database and call it `recipes`

7. Run the application with app.py

8. You can visit the website at `http://127.0.0.1:5000`


### Heroku Deployment

1. Log into heroku (the terminal command: `heroku login`)

2. Create a new app on the [Heroku website](https://dashboard.heroku.com/apps) by clicking the "New" button in your dashboard. Give it a name and set the region to Europe (or type in the terminal prompt: `heroku apps:create <name of your app>`)

3. Create a `requirements.txt` file using the terminal command `python -m pip freeze --local > requirements.txt`.

4. Create a `Procfile` with the terminal command `echo web: python app.py > Procfile`.

5. Create a git repository (the terminal: `git init`) 

6. Then `git add .` , `git commit -m "Initial deployment"`, `git push` the project to GitHub.

7. Now you need to link heroku with git, using the terminal type:
`git remote add heroku <Heroku Git URL`
`git push -u heroku master`
`The URL you can get in the Settings`

8. In the heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".

9. Set the following config vars:

Key  |  Value  |
--- | ---
IP | 0.0.0.0
MONGO_URI | in Mongodb find `CONNECT`, `Connect Your Application` and modify the expression properly
PORT | 5000
SECRET_KEY | `<your_secret_key>`


## Credits

### Content

- The text for the recipes was copied from [BBC Food](https://www.bbc.co.uk/food).

- The images used in this site were obtained from [PEXELS](https://www.pexels.com/).

- The code was corrected using Stack Overflow, however it was significantly modified for the use of this project.

### Acknowledgements

I received inspiration for this project from several cooking website, especially [BBC goodfood](https://www.bbcgoodfood.com/recipes) and [allrecipes](https://www.allrecipes.com/).

## Disclaimer
The content of this website is educational purposes only.
