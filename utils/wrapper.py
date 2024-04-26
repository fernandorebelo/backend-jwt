from flask import request, jsonify
import jwt
from functools import wraps

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(' ')[1]
        print(request.headers)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            print(token)
            data = jwt.decode(token, 'KEEP_IT_A_SECRET', algorithms=['HS256'])
        except:
            return jsonify({'message': 'Invalid token'}), 403

        return func(*args, **kwargs)

    return decorated
