from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder="templates")

@app.route('/')
def home():
    with open("recipes.json", encoding="utf-8") as file:
        data = json.load(file)
    recipes = data["recipe"]
    recipeCount = len(recipes)
    sorted_recipes = sorted(recipes, key=lambda x: x["name"].lower())
    return render_template('HomePage.html', recipes=sorted_recipes, count=recipeCount)

@app.route('/<dishtype>')
def dishesPage(dishtype):
    with open("recipes.json", encoding="utf-8") as file:
        data = json.load(file)

    recipes = data["recipe"]
    thisDishes = [dish for dish in recipes if any(dishtype.lower() in k.lower() for k in dish["keys"])]
    if thisDishes:
        sortedDishes = sorted(thisDishes, key=lambda x: x['name'].lower())
        return render_template('recipeList.html', dishes=sortedDishes, dishType = dishtype)
    else:
        return "Page not found :(?"

@app.route('/<dishtype>/<recipe>')
def dishes(dishtype, recipe):
    with open("recipes.json", encoding="utf-8") as file:
        data = json.load(file)

    recipes = data["recipe"]
    thisRecipe = next((rcp for rcp in recipes if rcp["name"] == recipe), None)

    if thisRecipe:
        return render_template('Foodrecipe.html', recipe=thisRecipe, dishType = dishtype)

@app.route('/lisaa-resepti')
def new_recipe():
    return render_template('AddRecipe.html')

@app.route('/lisaa-resepti', methods=['POST'])
def add_recipe():
    new_recipe = {
        "name": request.form.get("name"),
        "ingredients": request.form.get("ingredients").split("\n"),
        "instructions": request.form.get("instructions").split("\n"),
        "keys": request.form.get("keys").split(",")
    }

    with open("recipes.json", "r+") as file:
        data = json.load(file)
        data["recipe"].append(new_recipe)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    return render_template("AddedRecipe.html")

if __name__ == "__main__":
    app.run()