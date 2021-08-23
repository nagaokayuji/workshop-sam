# SAM で シンプルな API を作成してみる (ハンズオン)

## sam init: SAMテンプレートを作成

次のコマンドを実行してみましょう。

```bash
sam init
```

次のように聞かれるため、今回は以下のように選択してみます。

```bash
Which template source would you like to use?
	1 - AWS Quick Start Templates
	2 - Custom Template LocationWhich template source would you like to use?
	1 - AWS Quick Start Templates
	2 - Custom Template Location
Choice: 1
What package type would you like to use?
	1 - Zip (artifact is a zip uploaded to S3)
	2 - Image (artifact is an image uploaded to an ECR image repository)
Package type: 2

Which base image would you like to use?
	1 - amazon/nodejs14.x-base
	2 - amazon/nodejs12.x-base
	3 - amazon/nodejs10.x-base
	4 - amazon/python3.8-base
	5 - amazon/python3.7-base
	6 - amazon/python3.6-base
	7 - amazon/python2.7-base
	8 - amazon/ruby2.7-base
	9 - amazon/ruby2.5-base
	10 - amazon/go1.x-base
	11 - amazon/java11-base
	12 - amazon/java8.al2-base
	13 - amazon/java8-base
	14 - amazon/dotnet5.0-base
	15 - amazon/dotnetcore3.1-base
	16 - amazon/dotnetcore2.1-base
Base image: 4

Project name [sam-app]: workshop-sam

Cloning app templates from https://github.com/aws/aws-sam-cli-app-templates

AWS quick start application templates:
	1 - Hello World Lambda Image Example
	2 - PyTorch Machine Learning Inference API
	3 - Scikit-learn Machine Learning Inference API
	4 - Tensorflow Machine Learning Inference API
	5 - XGBoost Machine Learning Inference API
Template selection: 3
```

## テンプレートの確認

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

## sam build: ビルド

先ほど作成されたディレクトリへ移動し、次のコマンドを実行します。

```bash
sam build
```

以下のような表示になれば成功です。

```
(略)
Build Succeeded

Built Artifacts  : .aws-sam/build
Built Template   : .aws-sam/build/template.yaml

Commands you can use next
=========================
[*] Invoke Function: sam local invoke
[*] Deploy: sam deploy --guided
```

# ローカル環境で実行してみる

## Lambdaを実行

`sam local invoke`  コマンドによりローカル環境で実行することができます。

```bash
sam local invoke InferenceFunction --event events/event.json
```

実行結果は以下のようになります。

```
Invoking Container created from inferencefunction:python3.8-v1
Building image..........
Skip pulling image and use local one: inferencefunction:rapid-1.23.0.

START RequestId: f7a2ed16-5229-4174-8fdc-fcff84a64ab7 Version: $LATEST
END RequestId: f7a2ed16-5229-4174-8fdc-fcff84a64ab7
REPORT RequestId: f7a2ed16-5229-4174-8fdc-fcff84a64ab7	Init Duration: 1.02 ms	Duration: 2928.78 ms	Billed Duration: 3000 ms	Memory Size: 5000 MB	Max Memory Used: 5000 MB
{"statusCode": 200, "body": "{\"predicted_label\": 3}"}
```

## API を実行

`sam local start-api` コマンドを実行すると、ローカル環境で API サーバが立ち上がります。

パスについては `template.yml` の Resources セクション に記載します。

`http://127.0.0.1:3000/classify_digit`  がサンプルのエンドポイントとなります。

```bash
curl -X POST http://127.0.0.1:3000/classify_digit -d "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAAAAABXZoBIAAABQGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGDiSSwoyGFhYGDIzSspCnJ3UoiIjFJgf8rAyCDLIMQgxsCZmFxc4BgQ4ANUwgCjUcG3a0DVQHBZF2TWwmPutxO7FLa+827S7Tlpdx1TPQrgSkktTgbSf4A4IbmgqISBgTEGyFYuLykAsRuAbJEioKOA7CkgdjqEvQLEToKw94DVhAQ5A9kXgGyB5IzEFCD7AZCtk4Qkno7EhtoLAmxhwUYmFgQcSiooSa0oAdHO+QWVRZnpGSUKjsDQSVXwzEvW01EwMjAyZGAAhTVE9ecb4DBkFONAiMVeYmDQnwjyN0IsX5yB4RAHAwNPMUJM8w0DA18aA8NRtYLEokS4Axi/sRSnGRtB2NzbGRhYp/3//zmcgYFdk4Hh7/X//39v////7zIGBuZbDAwHvgEAq4heIf06wrwAAABWZVhJZk1NACoAAAAIAAGHaQAEAAAAAQAAABoAAAAAAAOShgAHAAAAEgAAAESgAgAEAAAAAQAAAH+gAwAEAAAAAQAAAIQAAAAAQVNDSUkAAABTY3JlZW5zaG90j9MWGwAAAYpJREFUeJy1kM0rRGEUxp/7uu64w+iaQphp8jHlIwkhH8lIaiQLZSE2NpKtZGHh35CUP8AWOwuKQkwmmUz5GLIRjTAxd65zLG5j7h2WnN3p1/Oc3/sC/zLSryv/gPkurX+SAYjr5V0AgJxG7qa+msL6KgBAsxB7KWvf7F5cJ2ZmMgxKrJVbk1LKo3E0LFNOpV8lZ5lqhbQtPB+XEcHCt9AiP4Sf7KK5eQ4BAOVbST6ZtAshZSqUDFXKiEWyIABI3oa+gFfQ0bEdiqJiJxUPD3vlz9uzU9igozHQVWFodcT0tLp+Y+/zbySIiJnJOBjIgT1J7x+cgiSRQ2npCT/YIMcWe5MxBucOzmiKyEoa0Rs2GMD9uMbIgoBuHvcpGROzQa0rMFelf8GdgTIA1T/WNH8BQHK3z3UrZJAF+pcCeSNXBCrtbKuVzrc3ny1Qay3Sp97BcHmcr0crh/d6+vUAqqeDjQBAby/R/d0d/fumBEAuDU50qI+34avHi1Dc+m+mbdtoWSQUumP80XwBdwyOoPfHcDkAAAAASUVORK5CYII="
```

- GUI からリクエストしてみる

Talend API Tester から画像を送信してみます。

[Talend API Tester - Free Edition](https://chrome.google.com/webstore/detail/talend-api-tester-free-ed/aejoelaoggembcahagimdiliamlcdmfm)

画像のサンプルは GitHub に載せてあります。

![https://res.cloudinary.com/ddaz9etkx/image/upload/v1628659111/ot/api_ni2woy.png](https://res.cloudinary.com/ddaz9etkx/image/upload/v1628659111/ot/api_ni2woy.png)

分類結果が返されることが確認できました。

# 実際にAWSにデプロイするまでの手順

## ECR にリポジトリを作成

コンテナイメージを使用する場合はリポジトリが必要になります。

DockerHub には対応していません。

手順に関しては以下に記載があります。

[Amazon ECR をAWS CLI](https://docs.aws.amazon.com/ja_jp/AmazonECR/latest/userguide/getting-started-cli.html)

- リポジトリを作成

```bash
aws ecr create-repository --repository-name workshop-sam-intro
```

- ECRにログイン

```bash
aws ecr get-login-password | docker login \
  --username AWS \
  --password-stdin ***********.dkr.ecr.ap-northeast-1.amazonaws.com/workshop-sam-intro
Login Succeeded
```

## sam deploy コマンドでデプロイ

`sam deploy` コマンドでデプロイが開始されます。

CloudFormation スタックの作成や ECRへのPushも行われます。

`sam deploy —guided` とすることでガイド付きのインタラクティブなモードになります。

実行してみます。

```bash
sam deploy --guided
```

いくつか質問されます。

> Stack Name

指定した名前で CloudFormation のスタックが作成されます。

今回は `workshop-sam-intro` と名前をつけておきます。

> InferenceFunction may not have authorization defined, Is this okay?

今回は認証を付けていないためこちらの質問には No と回答します。

```

Configuring SAM deploy
======================

        Looking for config file [samconfig.toml] :  Not found

        Setting default arguments for 'sam deploy'
        =========================================
        Stack Name [sam-app]: workshop-sam-intro                        
        AWS Region [ap-northeast-1]: 
        Image Repository for InferenceFunction: ************.dkr.ecr.ap-northeast-1.amazonaws.com/workshop-sam-intro
          inferencefunction:python3.8-v1 to be pushed to ************.dkr.ecr.ap-northeast-1.amazonaws.com/workshop-sam-intro:inferencefunction-4aaf9d3e4560-python3.8-v1

        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
        Confirm changes before deploy [y/N]: y
        #SAM needs permission to be able to create roles to connect to the resources in your template
        Allow SAM CLI IAM role creation [Y/n]: y
        InferenceFunction may not have authorization defined, Is this okay? [y/N]: y
        Save arguments to configuration file [Y/n]: y
        SAM configuration file [samconfig.toml]: 
        SAM configuration environment [default]: 
```

- CloudFormation の change set が表示されます。

```
CloudFormation stack changeset
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Operation                                 LogicalResourceId                         ResourceType                              Replacement                             
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
+ Add                                     InferenceFunctionInferencePermissionPro   AWS::Lambda::Permission                   N/A                                     
                                          d                                                                                                                           
+ Add                                     InferenceFunctionRole                     AWS::IAM::Role                            N/A                                     
+ Add                                     InferenceFunction                         AWS::Lambda::Function                     N/A                                     
+ Add                                     ServerlessRestApiDeployment50b627a8a5     AWS::ApiGateway::Deployment               N/A                                     
+ Add                                     ServerlessRestApiProdStage                AWS::ApiGateway::Stage                    N/A                                     
+ Add                                     ServerlessRestApi                         AWS::ApiGateway::RestApi                  N/A                                     
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

```

しばらく待つと完了します。

※ 実際にはアカウントIDも表示されています。

```
（略）
                                                                               
CREATE_COMPLETE                           AWS::CloudFormation::Stack                workshop-sam-intro                        -                                       
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Outputs                                                                                                                                                              
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Key                 InferenceApi                                                                                                                                     
Description         API Gateway endpoint URL for Prod stage for Inference function                                                                                   
Value               https://zz3wr4lyre.execute-api.ap-northeast-1.amazonaws.com/Prod/classify_digit/                                                                 

Key                 InferenceFunctionIamRole                                                                                                                         
Description         Implicit IAM Role created for Inference function                                                                                                 
Value               arn:aws:lambda:ap-northeast-1:************:function:workshop-sam-intro-InferenceFunction-nO6DAeNnjEfr                                            

Key                 InferenceFunction                                                                                                                                
Description         Inference Lambda Function ARN                                                                                                                    
Value               arn:aws:lambda:ap-northeast-1:************:function:workshop-sam-intro-InferenceFunction-nO6DAeNnjEfr                                            
----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Successfully created/updated stack - workshop-sam-intro in ap-northeast-1
```

API のエンドポイント `https://zz3wr4lyre.execute-api.ap-northeast-1.amazonaws.com/Prod/classify_digit/` が表示されているので、こちらにリクエストを送ってみます。

![https://res.cloudinary.com/ddaz9etkx/image/upload/v1628661865/ot/ag_ybbys9.png](https://res.cloudinary.com/ddaz9etkx/image/upload/v1628661865/ot/ag_ybbys9.png)

結果が得られ、デプロイされていることが確認できました。

## 作成したスタックを削除する

上記の手順で作成したAPIは公開しているため、最後に削除しておきます。

削除する場合は SAM ではなく CloudFormation から削除する必要があります。

`sam deploy` でデプロイした際に設定したスタック名を指定して削除します。

```
aws cloudformation delete-stack --stack-name workshop-sam-intro
```