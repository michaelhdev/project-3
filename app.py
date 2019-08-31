import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "place_names_site"
app.secret_key = os.urandom(24)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://root:r00tUser@myfirstcluster-bhsq8.mongodb.net/place_names_site?retryWrites=true&w=majority")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_place_names")
def get_place_names():
    return render_template("placeNames.html", place_names=mongo.db.place_names.find())

@app.route("/add_place_name")
def add_place_name():
    return render_template("addPlaceName.html",
                           locations=mongo.db.locations.find())
                           
@app.route("/insert_place_name", methods=["POST"])
def insert_place_name():
    place_names = mongo.db.place_names
    place_names.insert_one(request.form.to_dict())
    return redirect(url_for("get_place_names"))

@app.route("/edit_place_name/<place_name_id>")
def edit_place_name(place_name_id):
    the_place_name =  mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
    all_locations =  mongo.db.locations.find()
    return render_template("editPlaceName.html", place_name=the_place_name,
                           locations=all_locations) 

@app.route("/update_place_name/<place_name_id>", methods=["POST"])
def update_place_name(place_name_id):
    place_names = mongo.db.place_names
    place_names.update( {"_id": ObjectId(place_name_id)},
    {
        "eng_name":request.form.get("eng_name"),
        "irl_name":request.form.get("irl_name"),
        "irl_meaning": request.form.get("irl_meaning"),
        "history": request.form.get("history"),
        "location":request.form.get("location")
    })
    return redirect(url_for("get_place_names"))

@app.route("/delete_place_name/<place_name_id>")
def delete_place_name(place_name_id):
    mongo.db.place_names.remove({"_id": ObjectId(place_name_id)})
    return redirect(url_for("get_place_names"))
    
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
    mongo.db.locations.update(
        {"_id": ObjectId(location_id)},
        {"location_name": request.form.get("location_name")})
    return redirect(url_for("get_locations"))
    
@app.route("/delete_location/<location_id>")
def delete_location(location_id):
    mongo.db.locations.remove({"_id": ObjectId(location_id)})
    return redirect(url_for("get_locations"))
    
@app.route("/insert_location", methods=["POST"])
def insert_location():
    location_doc = {"location_name": request.form.get("location_name")}
    mongo.db.locations.insert_one(location_doc)
    return redirect(url_for("get_locations"))


@app.route("/add_location")
def add_location():
    return render_template("addLocation.html")
    
@app.route("/login_page")
def login_page():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login():
   
    users = mongo.db.users
    user = users.find_one({"userName": request.form["username"].lower()})
    
    if user:
        session['username'] = request.form['username'].lower()
        name = user["name"].split(" ")[0]
        session['name'] = name
       
        if user["admin"]=="True":
            session['admin'] = user["admin"]
        
        return redirect(url_for("get_place_names"))
    else:
        # user not found! -  Not registered/typo
        flash("Username '{}' is invalid.".format(request.form["username"]))
        return redirect(url_for("login_page"))
        
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('get_place_names'))
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)