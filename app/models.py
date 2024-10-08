from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Define metadata to be used by SQLAlchemy
metadata = MetaData()

# Initialize the SQLAlchemy instance with custom metadata
db = SQLAlchemy(metadata=metadata)

#Hero model
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    
    #columns for the Hero table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    super_name = db.Column(db.String)
    
    #relationship with HeroPower
    hero_powers = db.relationship('HeroPower', backref='hero')
    

    serialize_rules = ('-hero_powers.hero',)
    
    def __repr__(self):
        return f'<Hero {self.name} A.K.A {self.super_name}>'

#HeroPower model
class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    
    #relationships
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    
    #ensure strength is one of the allowed values
    @validates('strength')
    def validate_strength(self, key, value):
        strength_levels = ['Strong', 'Weak', 'Average']
        if value not in strength_levels:
            raise ValueError(f"Strength must be one of the following values: {strength_levels}")
        return value
    
    def __repr__(self):
        return f'<Hero-power {self.id} of {self.strength} strength>'

#Power model
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    # Exclude hero_powers attribute from serialized output to prevent circular references
    serialize_rules = ('-hero_powers.power',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    
    #relationship
    hero_powers = db.relationship('HeroPower', backref='power')
    
    #ensure description is at least 20 characters long
    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value
    
    def __repr__(self):
        return f'<Power: {self.name}. Description: {self.description}.>'
