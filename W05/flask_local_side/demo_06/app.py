# app.py

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", title="", name=name)

@app.route("/api/mydata", methods=['GET'])
def api_mydata_get():
    # access database
    my_data = {'data':{'T':28, 'H':80}, 'result':'OK', 'log':''}
    return jsonify(my_data)

@app.route("/api/mydata", methods=['POST'])
def api_mydata_post():
    # access database
    #my_data = {'data':{'T':28, 'H':80}, 'result':'OK', 'log':''}
    T = request.args.get('T')
    H = request.args.get('H')
    print('T=%s, H=%s' %(T, H))
    # insert data

    result = {'result': 'OK'}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8000)