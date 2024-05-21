from flask import Flask, jsonify, request
from flask_restful import Api
from database import db
import datetime
import jwt
import os
from flask_sqlalchemy import SQLAlchemy
from auth import auth



app = Flask(__name__)
api = Api(app) 

app.config['SECRET_KEY'] = os.environ.get('key')

db.init_app(app)

app.register_blueprint(auth)

users_db = {'chizzy@gmail.com': '88888'}
video_db = []

def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


@app.route('/videos', methods=["GET", "POST"])
def get_all():
    if (request.method == 'GET'):
        return jsonify(video_db)
    
    elif (request.method=='POST'):
         #authenticate the user
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing!'}), 403
        token = auth_header
        print('here')
        decoded_token = decode_token(token)
        print(decoded_token)
        print('done')
        if not decoded_token:
            return jsonify({'message': 'Token is invalid or expired!'}), 403
        
        # Get data from request parameters
        data = request.get_json()
        
        # check if all parameters are provided
        if not all([data.get('video_name'), data.get('video_id'), data.get('creator'), data.get('time_stamp')]):
            return jsonify({'message': 'Missing parameters'}), 400
        
        # check for duplicate id before adding it
        video_db.append(data)
    return jsonify({'message': 'successful'}), 200

@app.route('/videos/<video_id>')
def get_one(video_id):
    data = None
    for vid in video_db:
        if (vid['video_id'] == video_id):
            data = vid
    if not data:
        return jsonify({'message':'video not found'}), 404
    return jsonify(data)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.register_blueprint(auth)
    app.run(debug=True)