from flask_jwt_extended import create_access_token as flask_create_access_token

def generate_access_token(identity):
    return flask_create_access_token(identity=identity)
