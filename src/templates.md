# テンプレートの構成

サーバーレスアプリケーションのアーキテクチャを表す YAML 形式のファイルです。

AWS SAM のテンプレートファイルの構成は次のようになっています。

ほぼ CloudFormation と同じです。

```yaml
Transform: AWS::Serverless-2016-10-31 
# SAM を使用する場合は `Transform: AWS::Serverless-2016-10-31` を決まり文句として指定しておきます。
# これにより CloudFormation テンプレートが SAM のテンプレートとして識別されるようになります。
Globals: 
# SAM 固有のセクションです。
# 共通の関数やAPIのプロパティを定義することができます。
Description:
# ここにテンプレートの説明を書きます。
Metadata:
# メタデータを定義できます。
Parameters:
# テンプレートをデプロイする際に指定できるパラメータを定義できます。
Mappings:
# Key-Value 形式でパラメータを指定しておき、条件付きのパラメータとして使用することができます。
Conditions:
# 条件分岐を制御することができる条件を定義できます。
Resources: 
# 作成するリソースを記載します。
Outputs:
# 作成したリソースの属性などをスタックのプロパティから返される値として定義できます。
```

このうち、SAM を使用する上で必須なものは `Transform` と `Resources` のみです。

