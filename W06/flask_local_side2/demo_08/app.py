# app.py

from flask import Flask, render_template, jsonify, request, send_file
from firebase import firebase
import time
import random
import csv
from sqlalchemy import create_engine
import datetime
import openpyxl
from openpyxl.chart import LineChart, Reference

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

    result = {'result':'OK', 'config':'inv9,llll'}
    return jsonify(result)

@app.route("/api/iot", methods=['GET'])
def api_iot_get():
    # access database
    my_data = {'data':{'temp':28, 'humi':80, 'wind':1.5, 'co2':230}, 'result':'OK', 'log':''}
    return jsonify(my_data)

# 2023-02-11: 報表功能實作
@app.route("/api/khair/report", methods=['GET'])
def api_khair_report():

    mysql_db_url = 'mysql+pymysql://root:ixnqjmysql@209.97.161.199:43306/KH20221202_IoT_Data_Science'
    my_db = create_engine(mysql_db_url)

    table_name = 'malo_khair_1210'

    # 找出某個站的資料, 並排序: where, order
    sid = '前鎮國小'
    sql_cmd_str = "select * from %s where sid='%s' order by dtime ASC" %(table_name, sid)
    resultProxy=my_db.execute(sql_cmd_str)
    data = resultProxy.fetchall()
    #print('-- data --')
    #for item in data:
    #    print(dict(item))
        
    # write to csv
    fn = '%s_空氣品質.csv' %(sid)
    # 用utf-8時excel打開會有亂碼
    #with open(fn, 'w', newline='', encoding="utf-8") as csvfile:
    with open(fn, 'w', newline='', encoding="big5") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['=================================================='])
        writer.writerow(['  空氣品質報表'])
        writer.writerow(['=================================================='])

        writer.writerow(['時間', 'TSP'])
        tsp_list = list()
        for item in data:
            writer.writerow([ item['dtime'], item['tsp'] ])
            tsp_list.append(float(item['tsp']))
        writer.writerow(['平均值：', sum(tsp_list)/len(tsp_list)])

    print('make report!')
    #return send_file(fn, mimetype='text/xlsx', as_attachment=True) #如果是excel
    return send_file(fn, mimetype='text/csv', as_attachment=True)

# power meter
@app.route("/api/powermeter/report", methods=['GET'])
def api_powermeter_report():
    mysql_db_url = 'mysql+pymysql://root:ixnqjmysql@209.97.161.199:43306/KH20221202_IoT_Data_Science'
    my_db = create_engine(mysql_db_url)

    dt_now = datetime.datetime.now()
    #tm = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    date = dt_now.strftime("%Y-%m-%d") #'2023-02-11'
    t1 = date+' 00:00:00'
    t2 = date+' 23:59:59'

    sql_cmd_str = "select * from malo_khpower_1217 where (dtime>='%s') and (dtime<='%s') order by dtime ASC" %(t1, t2)
    resultProxy=my_db.execute(sql_cmd_str)
    histdata = resultProxy.fetchall()

    # 產生報表
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = '電力資訊'
    #寫入資料
    ws.append(['="========================================"'])
    ws.append(['  farm1電力資訊報表' ])
    ws.append(['="========================================"'])
    ws.append(['時間', 'v1', 'v2', 'v3', 'a1', 'a2', 'a3', 'total_e'])

    v1_list = list()
    v2_list = list()
    v3_list = list()
    a1_list = list()
    a2_list = list()
    a3_list = list()
    total_e_list = list()
    for item in histdata:
        dtime = item['dtime']
        v1 = item['v1']
        v2 = item['v2']
        v3 = item['v3']
        a1 = item['a1']
        a2 = item['a2']
        a3 = item['a3']
        total_e = item['total_e']
        ws.append([dtime, v1, v2, v3, a1, a2, a3, total_e])
        v1_list.append(float(v1))
        v2_list.append(float(v2))
        v3_list.append(float(v3))
        a1_list.append(float(a1))
        a2_list.append(float(a2))
        a3_list.append(float(a3))
        total_e_list.append(float(total_e))
        
    v1_avg = sum(v1_list)/len(v1_list)
    v2_avg = sum(v2_list)/len(v2_list)
    v3_avg = sum(v3_list)/len(v3_list)
    a1_avg = sum(a1_list)/len(a1_list)
    a2_avg = sum(a2_list)/len(a2_list)
    a3_avg = sum(a3_list)/len(a3_list)
    total_e_avg = sum(total_e_list)/len(total_e_list)
    ws.append(['="========================================"'])
    ws.append(['平均:', v1_avg, v2_avg, v3_avg, a1_avg, a2_avg, a3_avg, total_e_avg])

    #插入圖
    n = len(histdata)
    ref_data = Reference(ws, min_col=8, max_col=8, min_row=4, max_row=4+n)
    chart = LineChart()
    chart.add_data(ref_data, titles_from_data=True)
    chart.title = '趨勢圖'
    chart.x_axis.tilte = '時間'
    chart.y_axis.title = '累計電量'
    xtitle = Reference(ws, min_col=1, min_row=5, max_row=5+n-1)
    chart.set_categories(xtitle)
    ws.add_chart(chart, 'K4')

    #存檔
    fn = 'kh_power_report_day_chart.xlsx'
    wb.save(fn)
    return send_file(fn, mimetype='text/xlsx', as_attachment=True) #如果是excel


if __name__ == "__main__":
    app.run(debug=True, port=8000)