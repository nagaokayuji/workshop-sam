# DynamoDB を使用する

折角なので DynamoDB を使用してみます。

## 事前準備

以下にデータセットと設定が用意されています。

```bash
git clone git@github.com:nagaokayuji/workshop-sam.git
```

`dynamodb/docker-compose.yml` は以下のように定義されています。

```yaml
version: "3.8"
services:
  sam-dynamodb-local:
    image: amazon/dynamodb-local:1.16.0
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
    command: "-jar DynamoDBLocal.jar -sharedDb -optimizeDbBeforeStartup -dbPath ./data"
    networks:
      - workshop-sam
networks:
  workshop-sam:
    external: true
```

`workshop-sam` という名前の`network` が必要になるため、事前に作成します。

```bash
docker network create workshop-sam
```

`network`作成後、
以下コマンドで起動できます。

```bash
docker-compose -f dynamodb/docker-compose.yml up
```


## 作るもの

DynamoDB からデータを取得するAPIを追加します。

| path           | 内容                    |
| -------------- | ----------------------- |
| /athletes      | 全件取得                |
| /athletes/{id} | id を指定してデータ取得 |

## 関数を追加

今回はファイルを追加する形で作っていきたいと思います。

`app/`配下に `dynamo_app.py` という名前でファイルを作成します。

### DynamoDB の使用

Python から DynamoDB を使用するには次のようにします。

```python
import boto3
import decimal
from boto3.dynamodb.conditions import Key

# 環境変数からエンドポイントURLを取得
DYNAMODB_ENDPOINT = os.environ.get(
    "DYNAMODB_ENDPOINT", "http://localhost:8000")

# Resource API を使用
dynamodb = boto3.resource(
    'dynamodb', endpoint_url=DYNAMODB_ENDPOINT)

table = dynamodb.Table('athlete')
```

作成した table オブジェクトから次のようにオペレーションを実行することができます。

```python
table.scan() # scan を実行
```

今回作成するAPIでは path parameter が存在する場合は `Query`, 存在しない場合は `Scan`
を実行し、結果を返すようにします。

#### `dynamo_app.py` の全体

`type_handler` 関数は DynamoDB との型不整合を吸収するためのものです。

```python
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
```


## Dockerfile を変更

上記で作成した`dynamo_app.py` を docker イメージに追加していきます。

次の記述を`CMD ["app.lambda_handler"]` の上の行に追加します。

```docker
COPY dynamo_app.py ./
```


## `template.yml`を変更

API の path と 関数を設定します。

`template.yml` の `Resources`セクションに以下を追加します。

```yaml
  DynamoFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      ImageConfig:
        Command:
          - "dynamo_app.handler" # ファイル名・関数名
    #   Policies: AmazonDynamoDBFullAccess
      Environment:
        Variables:
          DYNAMODB_ENDPOINT: "http://sam-dynamodb-local:8000" # 作成したnetworkを指定する
      Events:
        ListAthletes: # リスト
          Type: Api
          Properties:
            Path: /athletes
            Method: get
        GetAthletes: # id 指定
          Type: Api
          Properties:
            Path: /athletes/{id}
            Method: get
    Metadata:
      Dockerfile: Dockerfile
      DockerContext: ./app
      DockerTag: python3.8-v1
```


以上でOKです。

## ビルド・実行

今までと同様にビルドします。

```bash
sam build
```

次に実行ですが、Local 環境の DynamoDB と接続するために `network` を指定する必要があります。

よって、次のコマンドで実行できます。

```bash
sam local start-api --docker-network workshop-sam
```

試してみましょう。

- 全件取得

```bash
curl http://localhost:3000/athletes
```


- ID指定
```bash
curl http://localhost:3000/athletes/12
```

次のようなレスポンスが得られれば成功です。
```json
{"Items": [{"NOC": "FIN", "Sex": "M", "index": 31.0, "City": "Sydney", "Weight": 70.0, "Name": "Jyri Tapani Aalto", "Sport": "Badminton", "Year": 2000.0, "Games": "2000 Summer", "Event": "Badminton Men's Singles", "Height": 172.0, "Team": "Finland", "ID": 12.0, "Medal": null, "Season": "Summer", "Age": 31.0}], "Count": 1, "ScannedCount": 1, "ResponseMetadata": {"RequestId": "e0be9c84-eb40-40e0-bea0-cb1ecd1930b7", "HTTPStatusCode": 200, "HTTPHeaders": {"date": "Sat, 28 Aug 2021 15:19:22 GMT", "content-type": "application/x-amz-json-1.0", "x-amz-crc32": "3814016791", "x-amzn-requestid": "e0be9c84-eb40-40e0-bea0-cb1ecd1930b7", "content-length": "405", "server": "Jetty(9.4.18.v20190429)"}, "RetryAttempts": 0}
```
