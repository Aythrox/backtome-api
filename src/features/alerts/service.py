import os
import boto3
import geohash2 as gh
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from src.features.alerts.model import Alert

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('ALERTS_TABLE')
table = dynamodb.Table(table_name) if table_name else None

def create_alert(alert_data: dict) -> Alert:
    alert = Alert(**alert_data)
    try:
        table.put_item(Item=alert.model_dump())
        return alert
    except ClientError as e:
        print(f"Error saving alert: {e}")
        raise e

def get_nearby_alerts(latitude: float, longitude: float) -> list[dict]:
    try:
        # Calculate the prefix for the search area
        # Precision 5 gives ~5x5 km area
        center_geohash = gh.encode(latitude, longitude, precision=5)
        
        response = table.query(
            IndexName='LocationIndex',
            KeyConditionExpression=Key('geohash_prefix').eq(center_geohash)
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error fetching nearby alerts: {e}")
        raise e
