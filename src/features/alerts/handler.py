import json
from src.features.alerts import service
from pydantic import ValidationError

def create_alert(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        alert = service.create_alert(body)
        return {
            "statusCode": 201,
            "body": json.dumps(alert.model_dump())
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

def get_nearby(event, context):
    try:
        query_params = event.get("queryStringParameters", {}) or {}
        lat_str = query_params.get("latitude")
        lon_str = query_params.get("longitude")
        
        if not lat_str or not lon_str:
            return {"statusCode": 400, "body": json.dumps({"message": "Missing latitude or longitude"})}
            
        latitude = float(lat_str)
        longitude = float(lon_str)
        
        alerts = service.get_nearby_alerts(latitude, longitude)
        return {
            "statusCode": 200,
            "body": json.dumps({"items": alerts})
        }
    except ValueError:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid latitude or longitude format"})}
    except Exception as e:
        print(f"Internal server error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error"})
        }
