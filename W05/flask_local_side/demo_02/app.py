from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello Flask</h1> <h2>12345678</h2>"

@app.route("/error")
def error():
    raise RuntimeError

@app.route("/error2")
def error2():
    return 10/0

if __name__ == "__main__":
    app.run(debug=True)