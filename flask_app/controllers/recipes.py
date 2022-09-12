from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


# -- ------------------------- (Create-recipe- Step 2 of 5) --------------------------->
@app.route("/new_recipe")
def create_recipe_form():
    if "user_id" not in session:
        return redirect("/") 
    return render_template("/create_recipe.html")

# -- ------------------------- (Create->recipe.py- Step 4 of 5) --------------------------->
@app.route("/submit_recipe", methods=["POST"])
def create_recipe():
    print(request.form)
    # logged in Validation
    if "user_id" not in session:
        return redirect("/") 
    # ----------------------- Validation  (planets.py-step 2 of 3)----------------------------
    if not Recipe.validate_recipe(request.form):
        return redirect("/new_recipe")
    data = {
        "name": request.form['name'],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30": request.form["under_30"],
        "user_id": session["user_id"]
    }
    Recipe.create(data)
    return redirect("/recipes")

#---------------------Delete Recipe (step 2 of 3))--------------------------------------
@app.route("/delete_recipe/<int:id>", methods=["POST"])
def delete_recipe(id):
    print(request.form)
    data = {
        "id": id
    }
    Recipe.delete(data)
    return redirect("/recipes")

# ---------------------Read one recipe (step 2 of 3)-----------------------
@app.route("/view_recipe/<int:id>") 
def view_recipe(id):
    data = {
        "id": id 
    }
    user_data = {
        "id" : session["user_id"]
    }
    return render_template("view_recipe.html",logged_in_user = User.get_by_id(user_data),  one_recipe = Recipe.get_one_with_user(data))


# -- -- ------ (update->edit_recipe.html- Step 2 of 5) --------------------------->
@app.route("/edit_recipe/<int:id>")
def edit_recipe(id):
    data = {
        "id": id
    }
    return render_template("edit_recipe.html", one_recipe = Recipe.get_one_with_user(data))

# -- -- ------ (update->recipe.py- Step 4 of 5) --------------------------->
@app.route("/update_recipe/<int:id>", methods = ["POST"])
def update_recipe(id):
    print(request.form)
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit_recipe/{id}")
    data = {
        "id": id,
        "name": request.form['name'],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30": request.form["under_30"],
        # "user_id": session["user_id"]
    }
    Recipe.update(data)
    return redirect("/recipes")