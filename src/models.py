from db import db

ships = db.Table('ships',
    db.Column('starship_id', db.Integer, db.ForeignKey('starships.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True)
)

fav_planets = db.Table('fav_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planets.id'), primary_key=True)
)

fav_characters = db.Table('fav_characters',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('char_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)

    favorite_planets = db.relationship('Planet', secondary=fav_planets, lazy='dynamic')
    favorite_characters = db.relationship('Character', secondary=fav_characters, lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }
    
    def favorite_list(self):
        return {
            "favorites": [fav.name for _ in (self.favorite_planets, self.favorite_characters) for fav in _]
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Character(db.Model):
    __tablename__ = 'characters'
    # Here we define columns for the table characters
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    height = db.Column(db.Float)
    mass = db.Column(db.Float)
    hair_color = db.Column(db.String(100))
    skin_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    gender = db.Column(db.String(100))

    homeworld_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    homeworld = db.relationship('Planet', backref="residents")

    starships = db.relationship('Starship', secondary=ships, backref="pilots", lazy='dynamic')


    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "sking_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld.name,
            "starships": [starship.name for starship in self.starships],
            "id": self.id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Planet(db.Model):
    __tablename__ = 'planets'
    # Here we define columns for the table planets.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    rotation_period = db.Column(db.Float)
    orbital_period = db.Column(db.Float)
    diameter = db.Column(db.Float)
    climate = db.Column(db.String(100))
    gravity = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    surface_water = db.Column(db.Float)
    population = db.Column(db.BigInteger)



    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "residents": [{"name": character.name, "id": character.id} for character in self.residents],
            "id": self.id
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

class Starship(db.Model):
    __tablename__ = 'starships'
    # Here we define columns for the table starships.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    cost_in_credits = db.Column(db.BigInteger)
    length = db.Column(db.Float)
    max_atmosphering_speed = db.Column(db.Float)
    crew = db.Column(db.BigInteger)
    passengers = db.Column(db.BigInteger)
    cargo_capacity = db.Column(db.Float)
    consumables = db.Column(db.String(100))
    hyperdrive_rating = db.Column(db.Float)
    MGLT = db.Column(db.Integer)
    starship_class = db.Column(db.String(100))

    def __repr__(self):
        return '<Starship %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "starship_class": self.starship_class,
            "pilots": [{"name": character.name, "id": character.id} for character in self.pilots],
            "id": self.id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()