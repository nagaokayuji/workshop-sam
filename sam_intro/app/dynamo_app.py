import json
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Key


DYNAMODB_ENDPOINT = os.environ.get(
    "DYNAMODB_ENDPOINT", "http://localhost:8000")

dynamodb = boto3.resource(
    'dynamodb', endpoint_url=DYNAMODB_ENDPOINT)

table = dynamodb.Table('athlete')


def type_handler(x):
    return float(x) if isinstance(x, decimal.Decimal) else None


def handler(event, context):
    path_parameters = event.get('pathParameters')
    if path_parameters is None:
        return {
            'statusCode': 200,
            'body':
                json.dumps(table.scan(), default=type_handler)
        }
    else:
        id = int(path_parameters.get('id'))
        return {
            'statusCode': 200,
            'body':
                json.dumps(table.query(
                    KeyConditionExpression=Key('ID').eq(id)
                ), default=type_handler)
        }
