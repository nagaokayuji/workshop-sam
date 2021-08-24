# APIを追加してみる

これまで、サンプルのプロジェクトを使用して動作確認ができました。

では、APIを追加してみましょう。

## app.py に追加ハンドラを追加

サンプルと同じ`app.py`に以下のような関数を追加してみます。

正常に呼び出されれば `message: Hello world` が返ってきます。

```python
def hello_world(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "message": "Hello world"
            }
        )
    }
```

これをLambda関数として扱うため、テンプレートファイルのResourcesセクションに次の記述を追加します。

```yaml
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image # コンテナイメージ
      ImageConfig:
        Command:
          - "app.hello_world" # 実行する関数
      Events: # イベントソース
        Hello:
          Type: Api # API Gateway
          Properties:
            Path: /hello
            Method: get
    Metadata:
      Dockerfile: Dockerfile
      DockerContext: ./app
      DockerTag: python3.8-v1
```

このような数行の記述でAPIを追加することができます。

記述を追加したのち、`sam build` でビルドしておきましょう。

```bash
sam build
```

### Lambdaが実行できるか確認

先ほど定義した関数を実行してみます。

まず、Lambdaを`invoke`できるか見てみます。

```bash
sam local invoke HelloFunction
```

実行すると以下のような結果が得られ、正しくLambda関数として定義できたことがわかります。

```
Invoking Container created from inferencefunction:python3.8-v1Building image.................Skip pulling image and use local one: inferencefunction:rapid-1.29.0.START RequestId: 24a9a3da-fa47-4c8b-8440-236fc95804ad Version: $LATESTEND RequestId: 24a9a3da-fa47-4c8b-8440-236fc95804adREPORT RequestId: 24a9a3da-fa47-4c8b-8440-236fc95804ad  Init Duration: 0.92 ms  Duration: 2816.10 ms    Billed Duration: 2900 ms     Memory Size: 5000 MB    Max Memory Used: 5000 MB{"statusCode": 200, "body": "{\"message\": \"Hello world\"}"}b
```

### APIが実行できるか確認

次に、APIを立ち上げて確認してみます。

```bash
sam local start-api
```

`curl` でリクエストを送ってみます。

```bash
curl -X GET "http://localhost:3000/hello"
```

すると以下のように正常レスポンスが得られ、
APIの実行も問題ないことが確認できます。

```json
{"message": "Hello world"}
```

これにて追加のAPIを作成することができました。