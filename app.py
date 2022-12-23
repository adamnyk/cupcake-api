"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from secret import API_SECRET_KEY

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = API_SECRET_KEY
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# debug = DebugToolbarExtension(app)
app.app_context().push()

connect_db(app)


@app.route("/")
def show_homepage():
    '''Render homepage'''
    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes=cupcakes)    

# *****************************
# RESTFUL CUPCAKES JSON API
# *****************************
@app.route("/api/cupcakes")
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes/<int:id>")
def show_cupcake(id):
    """Returns JSON for a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods = ["POST"])
def make_cupcake():
    '''Adds new cupcake to database and returns JSON of the new cupcake.'''
    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"], 
        rating=request.json["rating"], 
        image=request.json["image"] or None)
    
    db.session.add(new_cupcake)
    db.session.commit()
    
    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:id>", methods = ["PATCH"])
def update_cupcake(id):
    '''Updates a specific cupcake and returns JSON of that cupcake.'''
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods = ["DELETE"])
def delete_cupcake(id):
    '''Deletes a specific cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message="deleted")




