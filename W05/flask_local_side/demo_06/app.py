# app.py

from flask import Flask, render_template, jsonify, request
from firebase import firebase
import time
import random

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

@app.route("/api/firebase/log2", methods=['GET'])
def api_firebase_log2_get():
    # do something
    tag_name = '/tag_malo'
    my_firebase = firebase.FirebaseApplication('https://fire-test-c46d1.firebaseio.com', None)
    my_data = my_firebase.get(tag_name, 'log2')
    result = {'result':'OK', 'data':my_data}
    return jsonify(result)
    

@app.route("/api/firebase/log2", methods=['POST'])
def api_firebase_log2_post():
    # do something
    tag_name = '/tag_malo'
    my_firebase = firebase.FirebaseApplication('https://fire-test-c46d1.firebaseio.com', None)
    my_time = time.strftime("%Y-%m-%d %H:%M:%S")
    my_data = {'data': {'T': round(random.uniform(25, 30), 1), 
                        'H': round(random.uniform(50, 90), 1)}, 'time': my_time}
    my_firebase.put(tag_name+'/log2', my_time, my_data)

    result = {'result':'OK'}
    return jsonify(result)

@app.route("/api/iot", methods=['GET'])
def api_iot_get():
    # access database
    my_data = {'data':{'temp':28, 'humi':80, 'wind':1.5, 'co2':230}, 'result':'OK', 'log':''}
    return jsonify(my_data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)