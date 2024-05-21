from flask import Flask, Blueprint, request, jsonify
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from database import User, db
import jwt
import validators
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('key')


auth = Blueprint("auth", __name__)
def create_token(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


 
 
@auth.route('/register', methods=["POST"])
def register():
    user= request.get_json()
    username = request.get("username")
    email = user.get("email")
    password = user.get("password")
    
    # validtion
    if not user or not password or not email or not username:
        return jsonify({'message': 'Provide valid username, email and password'}, 400)
    if len(password) < 5:
        return jsonify({'error':"Password is too short"}), 400
    
    if len(username) < 5:
        return jsonify({'error':"Username is too short"}), 400
    
    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), 400
    
    # check if email already exists
    if User.query.filter_by(email=email).first() is not None:
         return jsonify({'error': 'Email is taken'}), 409
    
    # check username already exits
    if User.query.filter_by(username=username).first() is not None:
         return jsonify({'error': 'Username is taken'}), 409
   
    # hashpassword, store in database
    pwd_hash=generate_password_hash(password)
    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Account created'}), 200
    
    
        
@auth.route('/login', methods = ["POST"])
def login():
    user = request.get_json()
    email = user.get("email")
    password = user.get("password")
    
    if not user or not password or not email:
        return jsonify({'message': 'Provide valid email and password'}, 400)
    token = create_token(email)
    return jsonify({'message': 'Login successful',
                    'token': token}), 200