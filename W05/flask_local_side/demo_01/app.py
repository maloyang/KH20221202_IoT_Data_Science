from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello Flask, Malo Here</h1> <br> <h2>new line</h2>"

if __name__ == "__main__":
    app.run()