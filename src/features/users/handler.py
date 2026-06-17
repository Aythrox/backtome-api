import json
from src.features.users import service
from pydantic import ValidationError

def create_user(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user = service.create_user(body)
        return {
            "statusCode": 201,
            "body": json.dumps(user.model_dump())
        }
    except ValidationError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input", "details": e.errors()})
        }
    except Exception as e:
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }

def get_user(event, context):
    try:
        path_parameters = event.get("pathParameters", {})
        user_id = path_parameters.get("id")
        
        if not user_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Missing user_id"})}
            
        user = service.get_user(user_id)
        if not user:
            return {"statusCode": 404, "body": json.dumps({"message": "User not found"})}
            
        return {
            "statusCode": 200,
            "body": json.dumps(user)
        }
    except Exception as e:
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
