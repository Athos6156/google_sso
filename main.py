from flask import Flask, redirect, url_for
from authlib.integrations.flask_client import OAuth
import jwt
import datetime

def create_jwt(user_info):
    # Define the payload of the JWT
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),  # Token expiry time
        'iat': datetime.datetime.utcnow(),  # Issued at time
        'sub': user_info['email']  # Subject of the token
    }

    return jwt.encode(payload, app.secret_key, algorithm='HS256')


app = Flask(__name__)
app.secret_key = 'Random secret key'  # Random secret key

# OAuth 2.0 client setup via Google's discovery URL
oauth = OAuth(app)
#See README
google = oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',  # Google discovery URL
    client_id='Your client ID',  # Replace with your client ID
    client_secret='Your client secret',  # Replace with your client secret
    client_kwargs={
        'scope': 'openid email profile',
        'issuer': 'https://accounts.google.com'  # Set the expected issuer
    },
)

@app.route('/')
def hello_world():
    return 'Welcome to Athos, log in -> <a href="/login">Google Login</a>'

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/callback')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('https://www.googleapis.com/oauth2/v3/userinfo')  # Corrected URL
    user_info = resp.json()
    # Create JWT for the user
    jwt_token = create_jwt(user_info)
    # Return the JWT token
    return {'jwt': jwt_token}


if __name__ == '__main__':
    app.run(debug=True)


