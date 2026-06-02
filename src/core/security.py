import json
import os
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests

JWT_SECRET = os.environ.get('JWT_SECRET', 'local-dev-secret-do-not-use-in-prod')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com')

def _generate_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def login_handler(event, context):
    """
    Endpoint for the mobile app to exchange a Google ID Token for our custom JWT.
    """
    try:
        body = json.loads(event.get('body', '{}'))
        token = body.get('id_token')

        if not token:
            return _generate_response(400, {"error": "Missing id_token"})

        # Verify Google ID token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # In a real app, you would upsert the user into the DynamoDB UsersTable here
        # user_id = idinfo['sub']
        # email = idinfo['email']
        # name = idinfo.get('name', '')
        
        user_id = idinfo['sub']

        # Generate custom JWT
        jwt_payload = {
            'user_id': user_id,
            'email': idinfo.get('email'),
            'role': 'user'
        }
        custom_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm='HS256')

        return _generate_response(200, {
            "token": custom_token,
            "user_id": user_id
        })

    except ValueError as e:
        # Invalid token
        return _generate_response(401, {"error": "Invalid Google token", "details": str(e)})
    except Exception as e:
        return _generate_response(500, {"error": "Internal server error", "details": str(e)})

def verify_jwt(token: str) -> dict:
    """
    Utility function for parsing and verifying our custom JWT.
    Used by middleware / Lambda Authorizer.
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
