import os
import json
import boto3
from typing import Optional

from .model import Sighting

# Init Boto3 clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

SIGHTINGS_TABLE = os.environ.get('SIGHTINGS_TABLE')
ALERTS_TABLE = os.environ.get('ALERTS_TABLE')
SNS_TOPIC_ARN = os.environ.get('SNS_NOTIFICATION_TOPIC_ARN')

def _get_alert_owner(alert_id: str) -> Optional[str]:
    """Fetch the alert to find the owner_id so we can notify them."""
    table = dynamodb.Table(ALERTS_TABLE)
    response = table.get_item(Key={'alert_id': alert_id})
    item = response.get('Item')
    if item:
        return item.get('owner_id')
    return None

def process_sighting(sighting: Sighting) -> Sighting:
    """
    Business logic for processing a new sighting.
    1. Saves it to DynamoDB.
    2. Sends a push notification to the owner.
    """
    # 1. Save to DynamoDB
    table = dynamodb.Table(SIGHTINGS_TABLE)
    table.put_item(Item=sighting.model_dump())

    # 2. Trigger Push Notification via SNS (to be picked up by push worker)
    owner_id = _get_alert_owner(sighting.alert_id)
    if owner_id and SNS_TOPIC_ARN:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps({
                "action": "NEW_SIGHTING",
                "alert_id": sighting.alert_id,
                "sighting_id": sighting.sighting_id,
                "owner_id": owner_id,
                "message": "Somebody may have spotted your pet!"
            })
        )

    return sighting
