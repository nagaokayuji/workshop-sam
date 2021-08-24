# サンプルアプリケーションの確認

`sam init` で生成されたプロジェクトは次のような構造になっています。

```
.
├── README.md
├── __init__.py
├── app
│   ├── Dockerfile
│   ├── __init__.py
│   ├── app.py
│   ├── model
│   └── requirements.txt
├── events
│   └── event.json
├── template.yml
└── training.ipynb
```

`training.ipynb` でモデルを作成（学習）しており、画像から数字を認識できるようです。

 `app.py` を呼び出すことで推論ができます。

`app` 配下に以下のような`Dockerfile`が生成されます。

```docker
FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./
COPY model /opt/ml/model

RUN python3.8 -m pip install -r requirements.txt -t .

CMD ["app.lambda_handler"]
```

## テンプレートファイルを確認

`template.yml` について見ていきます。

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 50
    MemorySize: 5000
  Api:
    BinaryMediaTypes:
      - image/png
      - image/jpg
      - image/jpeg

Resources:
  InferenceFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      PackageType: Image
      Events:
        Inference:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /classify_digit
            Method: post
    Metadata:
      Dockerfile: Dockerfile
      DockerContext: ./app
      DockerTag: python3.8-v1

Outputs:
  # ServerlessRestApi is an implicit API created out of Events key under Serverless::Function
  # Find out more about other implicit resources you can reference within SAM
  # https://github.com/awslabs/serverless-application-model/blob/master/docs/internals/generated_resources.rst#api
  InferenceApi:
    Description: "API Gateway endpoint URL for Prod stage for Inference function"
    Value: !Sub "https://\${ServerlessRestApi}.execute-api.\${AWS::Region}.amazonaws.com/Prod/classify_digit/"
  InferenceFunction:
    Description: "Inference Lambda Function ARN"
    Value: !GetAtt InferenceFunction.Arn
  InferenceFunctionIamRole:
    Description: "Implicit IAM Role created for Inference function"
    Value: !GetAtt InferenceFunction.Arn
```

### Resources セクション
`Resources` セクションでAPIを定義しています。

```yaml
Resources:
  InferenceFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      PackageType: Image
      Events:
        Inference:
          Type: Api # More info about API Event Source: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#api
          Properties:
            Path: /classify_digit
            Method: post
    Metadata:
      Dockerfile: Dockerfile
      DockerContext: ./app
      DockerTag: python3.8-v1
```

- `InferenceFunction` 
  - 定義するAPIの名前です。
- `AWS::Serverless::Function` 
  - Lambda 関数を作成することを意味します。
- `Events`
  - `Event source object` を定義します。
    - 関数を呼び出すトリガーです。
    - `Type: Api` とすることで API Gateway 経由で呼び出すことになります。[^1]
  - `Properties`
    - API のメソッドとパスを定義します。

---
[^1]: `AWS::Serverless::Api` を作成しなくても、Events で Api を設定しておけば暗黙的に作成してくれます。