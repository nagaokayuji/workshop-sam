FROM public.ecr.aws/lambda/python:3.8

COPY model /opt/ml/model
COPY app.py requirements.txt ./
RUN python3.8 -m pip install -r requirements.txt -t .

COPY dynamo_app.py ./
CMD ["app.lambda_handler"]
