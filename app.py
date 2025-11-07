from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Kubernetes World - New Version! (rollback!!!)"

@app.route("/healthz")
def healthz():
    return jsonify(version=os.getenv("APP_VERSION", "unknown"))

if __name__ == '__main__':
    # host='0.0.0.0'로 설정하여 컨테이너 외부에서 접근 가능하도록 합니다.
    # port=5000 (또는 원하는 포트)로 실행합니다.
    app.run(host='0.0.0.0', port=5000)