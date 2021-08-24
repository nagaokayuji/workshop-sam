# SAM で シンプルな API を作成してみる (ハンズオン)
## 今回扱うものについて

API Gateway + Lambda のシンプルなAPIを作成します。

## sam init: SAMテンプレートを作成

早速、適当な作業スペースで次のコマンドを実行してみましょう。

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
