# Lambdaコンテナイメージのサポートについて

2020年末より、AWS Lamba がコンテナイメージのデプロイに対応しました。今回はこちらの機能も使っていきます。

[AWS Lambda の新機能 - コンテナイメージのサポート | Amazon Web Services](https://aws.amazon.com/jp/blogs/news/new-for-aws-lambda-container-image-support/)

以下の言語のイメージが公開されています。

- Python
- Node.js
- Go
- Ruby
- Java
- .NET

また、[ベースイメージ](https://github.com/aws/aws-lambda-base-images) も公開されており、自由なカスタマイズが可能となっています。

## Lambdaでコンテナイメージを使用するメリット

- ローカル環境での確認が容易
- 大きなプログラムをデプロイできる（250 MB → **10 GB**）
    - 従来はパッケージ等を追加するとすぐに上限に達していた
    - Cloud9 上で zip ファイルを作成しレイヤーを追加するなどの手間が不要に

使い方は簡単です。

以下のようなイメージをビルドし ECR に Push しておき、Lambda 作成時にイメージを指定します。

```docker
FROM public.ecr.aws/lambda/python:3.8

COPY app.py ${LAMBDA_TASK_ROOT}

# 実行される関数
CMD [ "app.handler" ]
```
