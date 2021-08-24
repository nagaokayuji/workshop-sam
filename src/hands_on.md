# SAM で シンプルな API を作成してみる (ハンズオン)
## 今回扱うものについて

API Gateway + Lambda のシンプルなAPIを作成します。

## 事前準備

### Docker

インストールされていない場合は以下よりインストールをお願いします。

[Get Docker](https://docs.docker.com/get-docker/)

### AWS SAM CLI
SAM を使用するために AWS SAM CLI が必要となります。

macOS の場合は次のコマンドでインストールできると思います。(Homebrew)

```bash
brew tap aws/tap
brew install aws-sam-cli
```

インストール方法に関してはこちらに記載があります。

[AWS SAM CLI のインストール](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
