"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/users', methods=['POST'])
def post_users():

    name = request.json.get('name')
    lastname = request.json.get('lastname')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not email: return jsonify({ "status": False, "msg": "Email is required!"}), 400

    user = User.query.filter_by(email=email).first()
    if user: return jsonify({ "status": False, "msg": "Email already in use!"}), 400

    user = User.query.filter_by(username=username).first()
    if user: return jsonify({ "status": False, "msg": "username already in use!"}), 400

    user = User()
    user.name = name
    user.lastname = lastname
    user.username = username
    user.email = email
    user.password = password

    user.save()

    return jsonify(user.serialize()), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_selected_user(id):

    users = User.query.get(id)

    return jsonify(users.serialize()), 200

@app.route("/users/<int:user_id>/favorites", methods=['GET', 'POST'])
@app.route("/users/<int:user_id>/favorites/<int:favorite_id>", methods=['GET', 'PUT', 'DELETE'])
def favorites_by_user(user_id, favorite_id = None):
    if request.method == 'GET':
        if favorite_id is not None:
            favorite = Favorite.query.filter_by(user_id=user_id, id=favorite_id).first()
            if not favorite: return jsonify({ "status": False, "msg": "favorite not found!"}), 404
            return jsonify(favorite.serialize()), 200
        else:
            favorites = Favorite.query.filter_by(user_id=user_id)
            favorites = list(map(lambda favorite: favorite.serialize(), favorites))
            return jsonify(favorites), 200

    if request.method == 'POST':
        
        planet_id = request.json.get("planet_id")
        character_id = request.json.get("character_id")

        contact.planet_id = planet_id
        contact.character_id = character_id
        contact.save()

        return jsonify(favorite.serialize()), 200

        user.save()

        return jsonify(contact.serialize()), 201

    if request.method == 'PUT':

        planet_id = request.json.get("planet_id")
        character_id = request.json.get("character_id")

        contact.planet_id = planet_id
        contact.character_id = character_id
        contact.update()

        return jsonify(favorite.serialize()), 200

    if request.method == "DELETE":
        favorite = Favorite.query.filter_by(user_id=user_id, id=favorite_id).first()

        if not favorite: return jsonify({ "status": False, "msg": "favorite not found!"}), 404

        favorite.delete()

        return jsonify({ "status": True, "msg": "Favorite deleted!"}), 200

@app.route('/people', methods=['GET'])
def get_characters():
    people = Characters.query.all()
    people = list(map(lambda people: people.serialize(), people))

    return jsonify(people), 200


@app.route('/people', methods=['POST'])
def post_characters():

    name = request.json.get('name')
    birthday = request.json.get('birthday')
    sex = request.json.get('sex')
    species = request.json.get('species')
    height = request.json.get('height')
    mass = request.json.get('mass')

    character = Characters()
    character.name = name
    character.birthday = birthday
    character.sex = sex
    character.species = species
    character.height = height
    character.mass = mass

    character.save()

    return jsonify(character.serialize()), 201

@app.route('/people/<int:id>', methods=['GET'])
def get_single_character(id):

    people = Characters.query.get(id)

    return jsonify(people.serialize()), 200

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_character(id):

    character = Characters.query.get(id)

    if not character: return jsonify({ "status": False, "msg": "Character doesn't exists!"}), 404

    character.delete()

    return jsonify({ "status": True, "msg": "Character deleted!"}), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planets: planets.serialize(), planets))

    return jsonify(planets), 200


@app.route('/planets', methods=['POST'])
def post_planets():

    name = request.json.get('name')
    diameter = request.json.get('diameter')
    population = request.json.get('population')
    atmosphere = request.json.get('atmosphere')
    rotation_period = request.json.get('rotation_period')

    planets = Planets()
    planets.name = name
    planets.diameter = diameter
    planets.population = population
    planets.atmosphere = atmosphere
    planets.rotation_period = rotation_period

    planets.save()

    return jsonify(planets.serialize()), 201

@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):

    planets = Planets.query.get(id)

    return jsonify(planets.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
