import os
import operator
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

app.config["MONGO_DBNAME"] = 'online_cookbook'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
def home():
    """
    displays all recipes in alphaetical order on the home page.
    """
    recipes = mongo.db.recipes.find().sort('recipe_title')
    
    """
    Statistical table
    counts the amount of recipes for each kind of cuisine in the database. 
    """
    cuisines_all = mongo.db.recipes.find({},{'cuisine':1, '_id':0}).count()
    count_cuisines = mongo.db.recipes.aggregate([ {'$group': { '_id': {"cuisine": "$cuisine"}, 'count': {'$sum': 1} } } ])
    """
    Statistical table
    counts the amount of recipes for each kind of meal type. 
    """
    count_meals = mongo.db.recipes.aggregate([ {'$group': { '_id': {"meal_type": "$meal_type"}, 'count': {'$sum': 1} } } ])
    """
    Statistical table
    counts the amount of recipes for each rating score. 
    """
    five_counter = 0
    four_counter = 0
    three_counter = 0
    two_counter = 0
    one_counter = 0
    no_review_counter = 0
    veg_counter = 0
    
    for recipe in mongo.db.recipes.find({ "score": { "$exists": True } }):
            if (recipe["score"] // recipe["votes"]) == 5:
                five_counter += 1
            elif (recipe["score"] // recipe["votes"]) == 4:
                four_counter += 1
            elif (recipe["score"] // recipe["votes"]) == 3:
                three_counter += 1  
            elif (recipe["score"] // recipe["votes"]) == 2:
                two_counter += 1
            elif (recipe["score"] // recipe["votes"]) == 1:
                one_counter += 1
    """
    Statistical table
    counts the amount of vegetarian recipes. 
    """            
    for recipe in mongo.db.recipes.find({'votes': {'$exists' : False} }):
            no_review_counter += 1
    
    for recipe in mongo.db.recipes.find({'vegetarian': {'$exists' : True} }):
            if(recipe["vegetarian"] is not None):
                veg_counter += 1
    
    return render_template('home.html', recipes=recipes, cuisines_all=cuisines_all,count_cuisines=count_cuisines, five_counter=five_counter, four_counter=four_counter, three_counter=three_counter, two_counter=two_counter, one_counter=one_counter, no_review_counter=no_review_counter, veg_counter=veg_counter, count_meals=count_meals)

@app.route('/recipes_without_review', methods=['POST', 'GET'])
def recipes_without_review():
    """
    Homepage
    Statistical table
    finds the amount of recipes without the rating score.
    """
    recipes = mongo.db.recipes.find({'votes': {'$exists' : False} })
    count_cuisines = mongo.db.recipes.aggregate([ {'$group': { '_id': {"cuisine": "$cuisine"}, 'count': {'$sum': 1} } } ])
    return render_template('recipes.html',recipes=recipes, count_cuisines=count_cuisines)
    
@app.route('/reviewed_recipes', methods=['POST'])
def reviewed_recipes():
    """
    Homepage
    Statistical table
    finds the amount of recipes for each rating score from 1 to 5.
    """
    search_score = int(request.form.get('search_rate'))
    recipes = mongo.db.recipes.find({'votes': {'$exists' : True} })
    count_cuisines = mongo.db.recipes.aggregate([ {'$group': { '_id': {"cuisine": "$cuisine"}, 'count': {'$sum': 1} } } ])
    return render_template('reviewed_recipes.html', recipes=recipes, search_score=search_score, count_cuisines=count_cuisines)

@app.route('/vegetarian_recipes')
def vegetarian_recipes():
    """
    Homepage
    Statistical table
    finds the amount of vegetarian recipes .
    """
    recipes = mongo.db.recipes.find()
    return render_template('vegetarian_recipes.html', recipes=recipes)

    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    """
    finds the clicked recipe.
    """
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe=the_recipe)


@app.route('/review_recipe/<recipe_id>', methods=['POST'])
def review_recipe(recipe_id):
    """
    edit_recipe.html
    sends the rating score to the database and adds 1 to the "votes" value simultaneously.
    """
    recipe = mongo.db.recipes
    vote_int = int(request.form.get('vote'))
    recipe.update({'_id': ObjectId(recipe_id)},{'$inc': {"score": vote_int, "votes": 1}})
    if request.method == 'POST':
        flash('Thanks, we have received your vote!')
    return redirect(url_for('home'))

 

@app.route('/recipes', methods=['POST'])    
def recipes():
    """
    Navbar
    the search bar, 
    finds clicked recipe types from the cuisine and the meal type category  
    """
    search_title = request.form.get('search_name')
    mongo.db.recipes.create_index([('$**', 'text')])
    recipes = mongo.db.recipes.find({'$text': {'$search': search_title}})
    return render_template('recipes.html', recipes=recipes, search_title=search_title)
    
@app.route('/share_your_recipe')
def share_your_recipe():
    """
    Navbar
    takes to the form for a new recipe webpage.
    """
    return render_template('share_your_recipe.html')


@app.route('/insert_recipe', methods=['POST']) 
def insert_recipe ():
    """
    share_your_recipe.html
    sends the fullfilled form to the database.
    """
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    if request.method == 'POST':
        flash('Thanks, {}, we have received your recipe!'.format(request.form['author']))
    return redirect(url_for('home'))
 
 
@app.route('/update_recipe/<recipe_id>', methods=['POST','GET'])
def update_recipe(recipe_id):
    """
    edit_recipe.html
    takes to the form for updating or deleting.
    """
    recipes = mongo.db.recipes.find()
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('update_recipe.html', recipes=recipes, recipe=the_recipe)


@app.route('/update/<recipe_id>', methods=['POST'])
def update(recipe_id):
    """
    update_recipe.html
    sends the uodated form to the database.
    """
    recipe = mongo.db.recipes
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
    if request.method == 'POST':
        flash('Thanks, {}, your recipe has been updated!'.format(request.form['author']))        
    return redirect(url_for('home'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    """
    update_recipe.html
    removes the recipe from the database.
    """
    recipe = mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash('The recipe has been deleted!')
    return redirect(url_for('home'))   

    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),port=os.environ.get('PORT'),debug=True)
        