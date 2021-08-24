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
