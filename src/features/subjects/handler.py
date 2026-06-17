import json
from src.features.subjects import service
from pydantic import ValidationError

def create_subject(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        # Normally extract owner_id from JWT authorizer context here
        subject = service.create_subject(body)
        return {
            "statusCode": 201,
            "body": json.dumps(subject.model_dump())
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

def get_subject(event, context):
    try:
        path_parameters = event.get("pathParameters", {})
        subject_id = path_parameters.get("id")
        
        if not subject_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Missing subject_id"})}
            
        subject = service.get_subject(subject_id)
        if not subject:
            return {"statusCode": 404, "body": json.dumps({"message": "Subject not found"})}
            
        return {
            "statusCode": 200,
            "body": json.dumps(subject)
        }
    except Exception as e:
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }

def list_by_owner(event, context):
    try:
        # We can pass owner_id via path or query params, or extract from JWT authorizer context.
        # For now, let's use query string parameters.
        query_params = event.get("queryStringParameters", {}) or {}
        owner_id = query_params.get("owner_id")
        
        if not owner_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Missing owner_id parameter"})}
            
        subjects = service.list_subjects_by_owner(owner_id)
        return {
            "statusCode": 200,
            "body": json.dumps({"items": subjects})
        }
    except Exception as e:
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
