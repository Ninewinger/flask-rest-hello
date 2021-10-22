from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique= True)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique= True)
    characters_fav = db.relationship('Characters', secondary=favorite_char, lazy='subquery')
    planet_fav = db.relationship('Planets', secondary=favorite_plan, lazy='subquery')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def serialize_with_favorite(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "favorite": self.favorite.serialize()
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

"""
class Favorite(db.Model):
    __tablename__ = 'Favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    characters_fav = db.relationship('Characters', secondary=favorite_char, lazy='subquery', backref=db.backref('favorite', lazy=True))
    planet_fav = db.relationship('Planets', secondary=favorite_char, lazy='subquery', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<Favorite %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }

    def get_character(self):
        return list(map(lambda role: Characters.serialize(), self.roles))

    def get_planet(self):
        return list(map(lambda role: Planets.serialize(), self.roles))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
"""

class Planets(db.Model):
    __tablename__= "Planets"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    population = db.Column(db.String(250))
    atmosphere = db.Column(db.String(250))
    rotation_period = db.Column(db.String(250))

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "population": self.population,
            "atmosphere": self.atmosphere,
            "rotation_period": self.rotation_period,
            # do not serialize the password, its a security breach
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Characters(db.Model):
    __tablename__= "Characters"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250))
    birthday = db.Column(db.String(250))
    species = db.Column(db.String(250))
    sex = db.Column(db.String(250))
    height = db.Column(db.String(250))
    mass = db.Column(db.String(250))

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birthday": self.birthday,
            "species": self.species,
            "sex": self.sex,
            "height": self.height,
            "mass": self.mass,
            # do not serialize the password, its a security breach
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

favorite_char = db.Table('favorite_char',
    db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('Character.id'), primary_key=True)
)

favorite_plan = db.Table('favorite_plan',
    db.Column('favorite_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('Planet.id'), primary_key=True)
)