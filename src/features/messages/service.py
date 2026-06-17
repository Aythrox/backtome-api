import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from src.features.messages.model import Message

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('MESSAGES_TABLE')
table = dynamodb.Table(table_name) if table_name else None

# SNS for Push Notifications
sns = boto3.client('sns')
push_topic_arn = os.environ.get('PUSH_NOTIFICATION_TOPIC_ARN') # Optional for future Push Integration

def create_message(message_data: dict) -> Message:
    message = Message(**message_data)
    try:
        table.put_item(Item=message.model_dump())
        
        # Simulated push notification logic
        if push_topic_arn:
            sns.publish(
                TopicArn=push_topic_arn,
                Message=f"New message from {message.sender_id} regarding alert {message.alert_id}"
            )
            
        return message
    except ClientError as e:
        print(f"Error saving message: {e}")
        raise e

def list_messages_by_alert(alert_id: str) -> list[dict]:
    try:
        response = table.query(
            IndexName='AlertIndex',
            KeyConditionExpression=Key('alert_id').eq(alert_id)
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error fetching messages for alert: {e}")
        raise e
