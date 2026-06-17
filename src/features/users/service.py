import os
import boto3
from botocore.exceptions import ClientError
from src.features.users.model import User

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('USERS_TABLE')
table = dynamodb.Table(table_name) if table_name else None

def create_user(user_data: dict) -> User:
    user = User(**user_data)
    try:
        table.put_item(Item=user.model_dump())
        return user
    except ClientError as e:
        print(f"Error saving user: {e}")
        raise e

def get_user(user_id: str) -> dict:
    try:
        response = table.get_item(Key={'user_id': user_id})
        return response.get('Item')
    except ClientError as e:
        print(f"Error fetching user: {e}")
        raise e
