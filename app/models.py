from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__='heroes'
    
    id=db.Column(db.Integer,primary_key=True )
    name=db.Column(db.String, unique=True)
    super_name=db.Column(db.String)
    
    hero_powers=db.relationship('HeroPower', backref='hero')
    
    def __repr__(self):
        return f'<Hero {self.name} A.K.A {self.super_name}>'
    
    
class HeroPower(db.Model, SerializerMixin):
    __tablename__='hero_powers'
    
    id=db.Column(db.Integer, primary_key=True)
    strength=db.Column(db.String)
    
    hero_id=db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id=db.Column(db.Integer, db.ForeignKey('powers.id'))
    
    def __repr__(self):
        return f'<Hero-power {self.id} of {self.strength} strength>'
    
    
    
class Power(db.Model, SerializerMixin):
    __tablename__='powers'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String ,nullable=False)
    
    hero_powers=db.relationship('HeroPower',backref='power')
    
    def __repr__(self):
        return f'<Power: {self.name}. Description:{self.description}.>'





