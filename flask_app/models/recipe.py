from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.under_30 = data["under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.user_id = data["user_id"]
        self.chef = None

# -- ------------------------- (Create-recipe- Step 5 of 5) --------------------------->
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_cooked, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s);"
        results = connectToMySQL("recipes").query_db(query, data)
        print(results)
        return results

#---------------------Delete Recipe (step 3 of 3))--------------------------------------
    @classmethod
    def delete(cls, data): 
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        print(results)
        return results

# ---------------------Read one recipe (step 3 of 3)-----------------------
    @classmethod
    def get_one_with_user(cls, data): 
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL('recipes').query_db(query, data) 
        print(results)
        recipe = cls(results[0])
        user_data = {
            # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
            "id": results[0]['users.id'], 
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        # using circular imports we are calling on the user model file (user),  then the User class instance (User), and passing in the user_data from above 
        user_obj = user.User(user_data)
        # Associate the Recipe class instance with the User class instance by filling in the empty chef attribute in the Recipe class (self.chef = None)
        recipe.chef = user_obj
        return recipe

# -- -- ------------ Update (Step 5 of 5) --------------------------->
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under_30 = %(under_30)s WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data) 
        print(results)
        return results


# *****Associating Users in Classes*******
# classmethod that will get all recipes, and their one associated User that discovered it, A JOIN will be required for this to get all of the needed data.
    @classmethod
    def get_all_recipes_with_user(cls):
        # The MANY goes on the left hand side of the JOIN while the ONE goes on the right side of the JOIN
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL("recipes").query_db(query)
        print(results)
        # We have an empty list to hold all the recipes instances that have the user instance inside of them
        all_recipes = []
        for row in results:
            # Create a recipe class instance from the information from each db row
            one_recipe = cls(row)
            # Prepare to make a User class instance, we need to match up the data dictionary to the User class in models/user.py 
            user_data = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            # using circular imports we are calling on the user model file (user),  then the User class instance (User), and passing in the user_data from above 
            user_obj = user.User(user_data)
            # Associate the Recipe class instance with the User class instance by filling in the empty chef attribute in the Recipe class (self.chef = None)
            one_recipe.chef = user_obj
            # Append the Planet containing the associated User to your list of planets
            all_recipes.append(one_recipe)
        return all_recipes



# --------------------validation (step 3 of 3)-----------------------------------
    @staticmethod
    def validate_recipe(recipe): #planet is the form information that we are passing in
        is_valid = True
        if len(recipe["name"]) <2:
            flash("Recipe name is too short!")
            is_valid = False
        if len(recipe["description"]) <2:
            flash("description is too short!")
            is_valid = False
        if len(recipe["instructions"]) <6:
            flash("Instructions is too short!")
            is_valid = False
        # validation for date/time field - was something inputed 
        if len(recipe["date_cooked"]) < 1:
            flash("Need to fill in date.")
            is_valid = False
        # if len(recipe["under_30"]) < 1 :
        #     flash("Can you cook under 30 min?")
        #     is_valid = False
        if "under_30" not in recipe:
            flash("Can you cook under 30 min?")
            is_valid = False
        return is_valid
