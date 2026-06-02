import json
import sys
import os
from typing import Any
from pydantic import ValidationError

# Ensure root src is in path for lambda environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.security import verify_jwt
from .model import Sighting
from .service import process_sighting

def _generate_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def report_sighting(event: dict[str, Any], context: Any) -> dict:
    """
    HTTP POST handler for /sightings.
    Validates request, calls service layer, formats HTTP response.
    """
    # 1. Authenticate
    auth_header = event.get('headers', {}).get('authorization', '')
    if not auth_header.startswith('Bearer '):
        return _generate_response(401, {"error": "Missing or invalid authorization header"})
    
    token = auth_header.split(' ')[1]
    try:
        user_info = verify_jwt(token)
        spotter_id = user_info['user_id']
    except Exception as e:
        return _generate_response(401, {"error": "Unauthorized", "details": str(e)})

    # 2. Parse Body & Validate
    try:
        body = json.loads(event.get('body', '{}'))
        body['spotter_id'] = spotter_id
        sighting_data = Sighting(**body)
    except json.JSONDecodeError:
        return _generate_response(400, {"error": "Invalid JSON"})
    except ValidationError as e:
        return _generate_response(400, {"error": "Validation Error", "details": e.errors()})

    # 3. Call Service Layer
    try:
        sighting = process_sighting(sighting_data)
        return _generate_response(201, {
            "message": "Sighting reported successfully", 
            "data": sighting.model_dump()
        })
    except Exception as e:
        # Catch unexpected business logic errors
        return _generate_response(500, {"error": "Internal Server Error", "details": str(e)})
