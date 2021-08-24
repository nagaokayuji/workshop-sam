# Lambdaコンテナイメージのサポートについて

2020年末より、AWS Lamba がコンテナイメージのデプロイに対応しました。

これが非常に便利なので今回はこちらの機能も使っていきます。

- [AWS Lambda の新機能 - コンテナイメージのサポート | Amazon Web Services](https://aws.amazon.com/jp/blogs/news/new-for-aws-lambda-container-image-support/)

Lambda では以下の言語のイメージが公開されています。

- Python
- Node.js
- Go
- Ruby
- Java
- .NET

また、[ベースイメージ](https://github.com/aws/aws-lambda-base-images) も公開されており、自由なカスタマイズが可能となっています。

## Lambdaでコンテナイメージを使用するメリット

コンテナイメージを使用することで次のようなメリットがあります。

- ローカル環境での確認が容易
- 大きなプログラムをデプロイできる（250 MB → **10 GB**）
    - 従来はパッケージ等を追加するとすぐに上限に達していた
    - Cloud9 で zip ファイルを作成しレイヤーを追加するなどの手間が不要に

## デメリット

- 単純な関数をデプロイしたい場合は逆に面倒
  - コンソールや AWS CLI からデプロイしてすぐに実行するほうが速い
- ECRにレポジトリを作らないといけない
