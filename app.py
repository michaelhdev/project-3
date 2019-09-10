import os
import sys
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
app.config["MONGO_DBNAME"] = "place_names_site"
app.secret_key = os.urandom(24)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://root:r00tUser@myfirstcluster-bhsq8.mongodb.net/place_names_site?retryWrites=true&w=majority")

mongo = PyMongo(app)


#######################################Helper Functions######################################################
""" These functions are used to ensure that there is no duplicate data in the database before adding or editing
    users, locations or place names"""
    
def valid_user():
    username = request.form.get("user_name")
    if mongo.db.users.find_one({"userName": username}) is None:
        return True
    else:
        return False

        
def valid_location():
    locationName = request.form.get("location_name")
    if mongo.db.locations.find_one({"location_name": locationName}) is None:
        return True
    else:
        return False
        
def valid_place_name():
    engName = request.form.get("eng_name")
    if mongo.db.place_names.find_one({"eng_name": engName}) is None:
        return True
    else:
        return False
    
##########################################View Functions for place names###################################################
""" These functions provide the functionality to - view place names, add a place name, edit a place name and delete a place name"""


@app.route("/")
@app.route("/get_place_names")
def get_place_names():
    #active_place_name is the place name that is been added or edited -> allows the page to scroll to the correct point
    return render_template("placeNames.html", place_names=mongo.db.place_names.find(), active_place_name="Initial")

@app.route("/add_place_name")
def add_place_name():
    return render_template("addPlaceName.html",
                           locations=mongo.db.locations.find())
                           
@app.route("/insert_place_name", methods=["POST"])
def insert_place_name():
    
    if valid_place_name():
        place_names = mongo.db.place_names
        place_names.insert_one(
        {
            "eng_name":request.form.get("eng_name"),
            "irl_name":request.form.get("irl_name"),
            "irl_meaning": request.form.get("irl_meaning"),
            "history": request.form.get("history"),
            "location":request.form.get("location"),
            "created_by":session['username'],
            "likes":0
        })
        the_active_place_name =request.form.get("eng_name")
        the_place_names =  mongo.db.place_names.find()
        return render_template("placeNames.html", place_names=the_place_names, active_place_name=the_active_place_name)
    else:
        #If its not a valid place name add error and return to page
        flash("Place Name '{}' already exists!".format(request.form.get("eng_name")))
        return redirect(url_for("add_place_name"))
    
    

@app.route("/edit_place_name/<place_name_id>")
def edit_place_name(place_name_id):
    the_place_name =  mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
    all_locations =  mongo.db.locations.find()
    return render_template("editPlaceName.html", place_name=the_place_name,
                           locations=all_locations) 

@app.route("/update_place_name/<place_name_id>", methods=["POST"])
def update_place_name(place_name_id):
    
    #Checks to see if the primary key of the record has changed, if it has check to see if there is a conflicting name in the database
    #If not update the record else display an error
    if request.form.get("original_eng_name") == request.form.get("eng_name"):
        place_names = mongo.db.place_names
        place_names.update( {"_id": ObjectId(place_name_id)},{"$set" :
            {
                "eng_name":request.form.get("eng_name"),
                "irl_name":request.form.get("irl_name"),
                "irl_meaning": request.form.get("irl_meaning"),
                "history": request.form.get("history"),
                "location":request.form.get("location")
            }})
        place_name = mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
        the_active_place_name = place_name["eng_name"]
        the_place_names =  mongo.db.place_names.find()
        return render_template("placeNames.html", place_names=the_place_names, active_place_name=the_active_place_name)
    else:
        if valid_place_name():
            place_names = mongo.db.place_names
            place_names.update( {"_id": ObjectId(place_name_id)},{"$set" :
            {
                "eng_name":request.form.get("eng_name"),
                "irl_name":request.form.get("irl_name"),
                "irl_meaning": request.form.get("irl_meaning"),
                "history": request.form.get("history"),
                "location":request.form.get("location")
            }})
            place_name = mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
            the_active_place_name = place_name["eng_name"]
            the_place_names =  mongo.db.place_names.find()
            return render_template("placeNames.html", place_names=the_place_names, active_place_name=the_active_place_name)
        else:
            flash("Place Name '{}' already exists!".format(request.form.get("eng_name")))
            return redirect(url_for("add_place_name"))
    
     

@app.route("/delete_place_name/<place_name_id>")
def delete_place_name(place_name_id):
    mongo.db.place_names.remove({"_id": ObjectId(place_name_id)})
    return redirect(url_for("get_place_names"))
    
@app.route("/sort_place_names", methods=["POST"])
def sort_place_names():
    #Sorts the results from the database based on the users selection
    #sorts decending if likes is selected ascending otherwise
    sortBy = request.form.get("sort_by")
    if sortBy == "likes":
        return render_template("placeNames.html", place_names=mongo.db.place_names.find().sort( sortBy ,-1), active_place_name="Initial")
    else:
        return render_template("placeNames.html", place_names=mongo.db.place_names.find().sort( sortBy ,1), active_place_name="Initial")
##########################################View functions for location##########################
""" These functions provide the functionality to - view locations, add a location, edit a location and delete a location"""
    
@app.route("/get_locations")
def get_locations():
    return render_template("locations.html",
                           locations=mongo.db.locations.find())  
                           
@app.route("/edit_location/<location_id>")
def edit_location(location_id):
    return render_template("editLocation.html",
                           location=mongo.db.locations.find_one(
                           {"_id": ObjectId(location_id)}))


@app.route("/update_location/<location_id>", methods=["POST"])
def update_location(location_id):
    
    #Checks to see if the primary key of the record has changed, if it has check to see if there is a conflicting name in the database
    #If not update the record else display an error
    if request.form.get("original_location") == request.form.get("location_name"):
        mongo.db.locations.update(
        {"_id": ObjectId(location_id)},
        {"location_name": request.form.get("location_name")})
        mongo.db.place_names.update( {"location": request.form.get("location_name")})
        return redirect(url_for("get_locations"))
    else:
        if valid_location():
            mongo.db.locations.update(
            {"_id": ObjectId(location_id)},
            {"location_name": request.form.get("location_name")})
            return redirect(url_for("get_locations"))
        else:
            flash("Location Name '{}' already exists!".format(request.form.get("location_name")))
            return redirect(url_for("edit_location", location_id=location_id))
        
    
@app.route("/delete_location/<location_id>")
def delete_location(location_id):
    location=mongo.db.locations.find_one({"_id": ObjectId(location_id)})
   
    mongo.db.locations.remove({"_id": ObjectId(location_id)})
    
    #delete and place names that have been assigned the location
    mongo.db.place_names.remove({"location": location["location_name"]})
    return redirect(url_for("get_locations"))
    
@app.route("/insert_location", methods=["POST"])
def insert_location():
    if valid_location():
        location_doc = {"location_name": request.form.get("location_name")}
        mongo.db.locations.insert_one(location_doc)
        return redirect(url_for("get_locations"))
    else:
        flash("Location Name '{}' already exists!".format(request.form.get("location_name")))
        return redirect(url_for("add_location"))

@app.route("/add_location")
def add_location():
    return render_template("addLocation.html")
###########################################View functions for user##################
""" These functions provide the functionality to - view users, add a user, edit a user and delete a user"""
    
@app.route("/get_users")
def get_users():
    return render_template("users.html",
                           users=mongo.db.users.find())  

@app.route("/add_user")
def add_user():
    return render_template("addUser.html")
    
@app.route("/insert_user", methods=["POST"])
def insert_user():
    
    if valid_user():
        user_doc = {"name": request.form.get("name"),"userName": request.form.get("user_name"),"dob": request.form.get("dob"),"admin": "False"}
        mongo.db.users.insert_one(user_doc)
        return redirect(url_for("get_users"))
    else:
        flash("User Name '{}' already exists!".format(request.form.get("user_name")))
        return redirect(url_for("add_user"))
                           
@app.route("/edit_user/<user_id>")
def edit_user(user_id):
    return render_template("editUser.html",
                           user=mongo.db.users.find_one(
                           {"_id": ObjectId(user_id)}))

@app.route("/update_user/<user_id>", methods=["POST"])
def update_user(user_id):
    
    #Checks to see if the primary key of the record has changed, if it has check to see if there is a conflicting name in the database
    #If not update the record else display an error
    if request.form.get("original_user_name") == request.form.get("user_name"):
       
        user_doc = {"name": request.form.get("name"),"userName": request.form.get("user_name"),"dob": request.form.get("dob"),"admin": "False"}
        mongo.db.users.update({"_id": ObjectId(user_id)}, user_doc)
        return redirect(url_for("get_users"))
        
    else:     
       
        if valid_user():
            user_doc = {"name": request.form.get("name"),"userName": request.form.get("user_name"),"dob": request.form.get("dob"),"admin": "False"}
            #Change to username on the place names table 
            mongo.db.place_names.update( {"created_by": request.form.get("original_user_name")}, { "$set": {"created_by": request.form.get("user_name")}}, multi=True)
            mongo.db.users.update({"_id": ObjectId(user_id)}, user_doc)
            return redirect(url_for("get_users"))
        else:
            flash("New User Name '{}' already exists!".format(request.form.get("user_name")))
            return redirect(url_for("edit_user", user_id=user_id))

    
@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    
    user=mongo.db.users.find_one({"_id": ObjectId(user_id)})
    #Remove and place names created by that user
    mongo.db.place_names.remove({"created_by": user["userName"]})
    
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    return redirect(url_for("get_users"))
    


#################################################View functions to login and logout############

@app.route("/login_page")
def login_page():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login():
   
    users = mongo.db.users
    user = users.find_one({"userName": request.form["username"].lower()})
    #If the username exists in the database set up the session data otherwise return to the page
    #and display an error
    if user:
        session['username'] = request.form['username'].lower()
        name = user["name"].split(" ")[0]
        session['name'] = name
       
        if user["admin"]=="True":
            session['admin'] = user["admin"]
        
        return redirect(url_for("get_place_names"))
    else:
        flash("Username '{}' is invalid.".format(request.form["username"]))
        return redirect(url_for("login_page"))
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('get_place_names'))

###############################################View functions to add likes###############################    
"""Toggles like or dislike and returns to the active place name in the page"""
@app.route("/add_like/<place_name_id>")
def add_like(place_name_id):
    place_name = mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
    current_likes = place_name["likes"]
    updated_likes = current_likes + 1
    mongo.db.place_names.update( {"_id": ObjectId(place_name_id)}, { "$set": {"likes": updated_likes}})
    the_active_place_name = place_name["eng_name"]
    the_place_names =  mongo.db.place_names.find()
    return render_template("placeNames.html", place_names=the_place_names, active_place_name=the_active_place_name) 
    
@app.route("/add_dislike/<place_name_id>")
def add_dislike(place_name_id):
    place_name = mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
    current_likes = place_name["likes"]
    updated_likes = current_likes - 1
    mongo.db.place_names.update( {"_id": ObjectId(place_name_id)}, { "$set": {"likes": updated_likes}})
    the_active_place_name = place_name["eng_name"]
    the_place_names =  mongo.db.place_names.find()
    return render_template("placeNames.html", place_names=the_place_names, active_place_name=the_active_place_name) 
    
###############################################################################


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)