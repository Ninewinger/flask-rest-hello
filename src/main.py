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
from models import User, Character, Planet, Starship
from db import db
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
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


# Users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": [user.serialize() for user in User.query.all()]})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.query.get(data['id'])
    if user:
        return jsonify({"message": f"User already exists."})
    user = User(**data)
    user.save()
    return jsonify({"message": f"User created."})

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    active_user = User.query.filter_by(is_active=1).first()
    planet = Planet.query.get(planet_id)
    if planet:
        active_user.favorite_planets.append(planet)
        active_user.save()
        return jsonify(planet.serialize())
    return jsonify({"message": f"planet with id: {planet_id} doesn't exists."})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    active_user = User.query.filter_by(is_active=1).first()
    character = Character.query.get(people_id)
    if character:
        active_user.favorite_characters.append(character)
        active_user.save()
        return jsonify(character.serialize())
    return jsonify({"message": f"character with id: {people_id} doesn't exists."})
        
@app.route('/users/favorites')
def show_favorites():
    user = User.query.filter_by(is_active=1).first()
    return jsonify(user.favorite_list())

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    active_user = User.query.filter_by(is_active=1).first()
    planet = Planet.query.get(planet_id)
    if planet:
        active_user.favorite_planets = [planet for planet in active_user.favorite_planets if planet_id != planet.id]
        active_user.save()
        return jsonify({"message" : f"planet with id: {planet_id} deleted."})
    return jsonify({"message": f"planet with id: {planet_id} doesn't exists."})

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    active_user = User.query.filter_by(is_active=1).first()
    character = Character.query.get(people_id)
    if character:
        active_user.favorite_characters = [character for character in active_user.favorite_characters if people_id != character.id]
        active_user.save()
        return jsonify({"message" : f"character with id: {people_id} deleted."})
    return jsonify({"message": f"character with id: {people_id} doesn't exists."})

# Characters
@app.route('/people')
def get_peoples():
    return jsonify({"characters": [character.serialize() for character in Character.query.all()]})

@app.route('/people', methods=['POST'])
def create_people():
    data = request.get_json()
    # unpack all data but 'starships'
    newChar = Character(**{key: value for key, value in data.items() if key != "starships"})
    # loop through array of starships_ids
    for ship_id in data['starships']:
        ship = Starship.query.get(ship_id)
        newChar.starships.append(ship)
    newChar.save()
    return jsonify({"message": f"character '{newChar.name}' created."})

@app.route('/people/<int:_id>')
def get_people(_id):
    character = Character.query.get(_id)
    if character:
        return jsonify(character.serialize())
    return jsonify({"message": f"character with id: {_id}, doesn't exists."})


# Planets
@app.route('/planets')
def get_planets():
    return jsonify({"planets": [planet.serialize() for planet in Planet.query.all()]})

@app.route('/planets/<int:_id>')
def get_planet(_id):
    planet = Planet.query.get(_id)
    if planet:
        return jsonify(planet.serialize())
    return jsonify({"message": f"planet with id: {_id}, doesn't exists."})

@app.route('/planet', methods=['POST'])
def create_planet():
    data = request.get_json()
    newPlanet = Planet(**data)
    newPlanet.save()
    return jsonify({"message": f"planet '{newPlanet.name}' created."})


# Starships
@app.route('/starships')
def get_starships():
    return jsonify({"starships": [starship.serialize() for starship in Starship.query.all()]})

@app.route('/starships', methods=['POST'])
def create_starship():
    data = request.get_json()
    newStarship = Starship(**data)
    newStarship.save()
    return jsonify({"message": f"starship '{newStarship.name}' created."})

@app.route('/starships/<int:_id>')
def get_starship(_id):
    starship = Starship.query.get(_id)
    if starship:
        return jsonify(starship.serialize())
    return jsonify({"message": f"starship with id: {_id}, doesn't exists."})



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)