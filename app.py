from flask import Flask, jsonify

from psycopg2 import connect
from json import loads
from os import getenv
from sys import stderr
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
    except:
        return None

    secret: str = get_secret_value_response["SecretString"]
    return loads(secret)


@app.route("/")
def hello():
    secret = get_secret()
    info = "not set"
    if secret is not None:
        info = secret["host"]
    return f"Hello World - 25.11.08 20:57 Version! {info}"


@app.route("/db")
def db_test():
    secret = get_secret()
    version = "not set"
    if secret is not None:
        with connect(
            host=secret["host"],
            port=secret["port"],
            dbname=secret["dbname"],
            user=secret["username"],
            password=secret["password"],
        ) as conn:
            cur = conn.cursor()
            cur.execute("select version();")
            version = cur.fetchone()[0]
            cur.close()
    return f"Hello, Postgresql : {version}"


@app.route("/health")
def health():
    return jsonify(version=getenv("APP_VERSION", "unknown"))


@app.route("/version")
def version():
    return jsonify(version=getenv("APP_VERSION", "unknown"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
