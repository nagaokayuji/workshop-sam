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
