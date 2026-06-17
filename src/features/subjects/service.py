import os
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from src.features.subjects.model import Subject

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('SUBJECTS_TABLE')
table = dynamodb.Table(table_name) if table_name else None

def create_subject(subject_data: dict) -> Subject:
    subject = Subject(**subject_data)
    try:
        table.put_item(Item=subject.model_dump())
        return subject
    except ClientError as e:
        print(f"Error saving subject: {e}")
        raise e

def get_subject(subject_id: str) -> dict:
    try:
        response = table.get_item(Key={'subject_id': subject_id})
        return response.get('Item')
    except ClientError as e:
        print(f"Error fetching subject: {e}")
        raise e

def list_subjects_by_owner(owner_id: str) -> list[dict]:
    try:
        response = table.query(
            IndexName='OwnerIndex',
            KeyConditionExpression=Key('owner_id').eq(owner_id)
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error fetching subjects by owner: {e}")
        raise e
