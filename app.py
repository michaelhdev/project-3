import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'place_names_site'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb+srv://root:r00tUser@myfirstcluster-bhsq8.mongodb.net/place_names_site?retryWrites=true&w=majority')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_place_names')
def get_place_names():
    return render_template("placeNames.html", place_names=mongo.db.place_names.find())

@app.route('/add_place_name')
def add_place_name():
    return render_template('addPlaceName.html',
                           locations=mongo.db.locations.find())
                           
@app.route('/insert_place_name', methods=['POST'])
def insert_place_name():
    place_names = mongo.db.place_names
    place_names.insert_one(request.form.to_dict())
    return redirect(url_for('get_place_names'))

@app.route('/edit_place_name/<place_name_id>')
def edit_place_name(place_name_id):
    the_place_name =  mongo.db.place_names.find_one({"_id": ObjectId(place_name_id)})
    all_locations =  mongo.db.locations.find()
    return render_template('editPlaceName.html', place_name=the_place_name,
                           locations=all_locations) 

@app.route('/update_place_name/<place_name_id>', methods=["POST"])
def update_place_name(place_name_id):
    place_names = mongo.db.place_names
    place_names.update( {'_id': ObjectId(place_name_id)},
    {
        'eng_name':request.form.get('eng_name'),
        'irl_name':request.form.get('irl_name'),
        'irl_meaning': request.form.get('irl_meaning'),
        'history': request.form.get('history'),
        'location':request.form.get('location')
    })
    return redirect(url_for('get_place_names'))

@app.route('/delete_place_name/<place_name_id>')
def delete_place_name(place_name_id):
    mongo.db.place_names.remove({'_id': ObjectId(place_name_id)})
    return redirect(url_for('get_place_names'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)