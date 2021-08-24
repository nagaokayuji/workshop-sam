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