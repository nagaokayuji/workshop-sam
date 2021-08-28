# %%
import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key
import decimal
import json
# %%

# 1000行のデータ
athlete_events = pd.read_csv(
    '.athlete_events_h1000.csv')
athlete_events

# %%
session = boto3.Session(aws_access_key_id='dummy',
                        aws_secret_access_key='dummy',
                        region_name='us-west-2')

# local 環境
dynamodb = session.resource('dynamodb', endpoint_url='http://localhost:8000')
# %%


def delete_table(dynamodb, table_name):
    try:
        table = dynamodb.Table(table_name)
        table.delete()
    except:
        pass


# %%

# %%
# テーブル作成
delete_table(dynamodb, 'athlete')
# %%
gust_table = dynamodb.create_table(
    TableName='athlete',
    KeySchema=[
        # partition key
        {'AttributeName': 'ID', 'KeyType': 'HASH'},
        # sort key
        {'AttributeName': 'index', 'KeyType': 'Range'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'ID', 'AttributeType': 'N'},
        {'AttributeName': 'index', 'AttributeType': 'N'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)
# %%
# データ追加
with gust_table.batch_writer() as batch:
    athlete_events.reset_index().apply(
        lambda row: batch.put_item(json.loads(row.to_json(), parse_float=decimal.Decimal)), axis=1
    )
# %%
