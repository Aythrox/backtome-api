import json
from src.features.messages import service
from pydantic import ValidationError

def create_message(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        message = service.create_message(body)
        return {
            "statusCode": 201,
            "body": json.dumps(message.model_dump())
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

def list_by_alert(event, context):
    try:
        query_params = event.get("queryStringParameters", {}) or {}
        alert_id = query_params.get("alert_id")
        
        if not alert_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Missing alert_id parameter"})}
            
        messages = service.list_messages_by_alert(alert_id)
        return {
            "statusCode": 200,
            "body": json.dumps({"items": messages})
        }
    except Exception as e:
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
