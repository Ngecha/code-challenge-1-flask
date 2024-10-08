from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Power, HeroPower, Hero

# Initialize Flask app
app = Flask(__name__)
# Set the database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///powers.db'
# Disable SQLAlchemy track modifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up database migration management
migrate = Migrate(app, db)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Route to get all heroes
@app.route('/heroes')
def heroes():
    heroes = []
    # Fetch all heroes from the database
    for hero in Hero.query.all():
        # Create a dictionary representation for each hero
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        heroes.append(hero_dict)
    response = make_response(heroes, 200)
    return response

# Route to get a hero by its id
@app.route('/heroes/<int:id>')
def hero_by_id(id):
    # Fetch the hero with the given id
    hero = Hero.query.filter(Hero.id == id).first()
    if hero:
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        body = hero_dict
        status = 200
    
    else:
        body = {"error": "Hero not found"}
        status = 404
        
    return make_response(body, status)

# Route to get all powers
@app.route('/powers')
def powers():
    powers = []
    # Fetch all powers from the database
    for power in Power.query.all():
        # Create a dictionary representation for each power
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name,
        }
        powers.append(power_dict)
   
    response = make_response(powers, 200)
    return response

# Route to get a power by its ID
@app.route('/powers/<int:id>')
def power_by_id(id):
    # Fetch the power with the given ID
    power = Power.query.filter(Power.id == id).first()
    
    if power:
        # If the power exists, create a dictionary for it
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name,
        }
        body = power_dict
        status = 200
    else:
        # If the power doesn't exist, return an error message
        body = {"error": "power not found"}
        status = 404
        
    return make_response(body, status)

# Route to update a power by its id using PATCH method
@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power_by_id(id):
    # Fetch the power with the given ID
    power = Power.query.filter(Power.id == id).first()
    
    if not power:
        # If the power doesn't exist, return an error message
        error_message = '"error":"Power not found"'
        return error_message
       
    try:
        # Update power attributes from the form data
        for attr in request.form:
            setattr(power, attr, request.form.get(attr))

        # Add the updated power to the session and commit
        db.session.add(power)
        db.session.commit()

        # Create a dictionary representation for the updated power
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name,
        }

        response = make_response(power_dict, 200)
        return response

    except ValueError:
        # Handle validation errors if they occur
        body = {"error": ["validation errors"]}
        status = 400
        return make_response(body, status)

# Route to create a new HeroPower
@app.route('/heropowers', methods=['POST'])
def create_hero_powers():
    try:
        # Create a new HeroPower from the form data
        new_power = HeroPower(
            strength=request.form.get('strength'),
            power_id=request.form.get('power_id'),
            hero_id=request.form.get('hero_id'),
        )
        # Add the new HeroPower to the session and commit
        db.session.add(new_power)
        db.session.commit()
    
        # Convert the new HeroPower to a dictionary using a method
        power_dict = new_power.to_dict()
    
        response = make_response(power_dict, 201)
        return response

    except ValueError:
        # Handle validation errors if they occur
        body = {"error": ["validation errors"]}
        status = 400
        return make_response(body, status)

# Run the app with debug mode enabled
if __name__ == '__main__':
    app.run(port=5555, debug=True)
