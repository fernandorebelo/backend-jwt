from flask import Flask, request, jsonify, make_response, render_template, session, flash, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
from utils.wrapper import token_required
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KEEP_IT_A_SECRET'
CORS(app)

@app.route('/public')
def public():
 return 'Public route. Anyone can access this.'

@app.route('/private')
@token_required
def auth():
  return 'JWT is verified. Welcome to your private page!'

@app.route('/login', methods=['GET','POST'])
def login():
    data = request.json
    user_name = data.get('username')
    user_password = data.get('password')

    if user_name == 'admin' and user_password == '123456':
        token = jwt.encode({
            'user': user_name,
            'expiration': str(datetime.utcnow() + timedelta(minutes=50)),
            'user_email': 'admin@admin.com',
            'user_phone': '111111111'
        }, 'KEEP_IT_A_SECRET', algorithm='HS256')

        return jsonify({'token': token, 'username': user_name, 'email': 'admin@admin.com', 'phone': '111111111'})
    else:
        return jsonify({'message': 'Invalid credentials'})


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))