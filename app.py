from flask import Flask, jsonify
from json import loads
from os import getenv
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)


def get_secret():
    secret_name = "prod/hackaton/db"
    region_name = "ap-northeast-1"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        return None

    secret: str = get_secret_value_response["SecretString"]
    return loads(secret)


@app.route("/")
def hello():
    secret = get_secret()
    flask_value = "not set"
    if secret is not None:
        flask_value = secret["flask"]
    return f"Hello, Kubernetes World - New Version! (rollback!!!) {flask_value}"


@app.route("/healthz")
def healthz():
    return jsonify(version=getenv("APP_VERSION", "unknown"))


if __name__ == "__main__":
    # host='0.0.0.0'로 설정하여 컨테이너 외부에서 접근 가능하도록 합니다.
    # port=5000 (또는 원하는 포트)로 실행합니다.
    app.run(host="0.0.0.0", port=5000)
