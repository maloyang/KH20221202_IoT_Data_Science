# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, send_file
import requests
import csv
import folium
import geocoder
from sqlalchemy import create_engine
from flask import json, jsonify
import datetime
import random

app = Flask(__name__)

mysql_db_url = 'mysql+pymysql://root:ixnqjmysql@209.97.161.199:43306/KH20221202_IoT_Data_Science'
my_db = create_engine(mysql_db_url)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name:
        return 'Hello! %s~' %(name)

    return 'Hello! Malo~'


@app.route('/hello/html')
def hello_html():
    html = '''<h1>你好</h1>
                <p style="background:red;"> malo's web site</p>'''
    return html


@app.route('/map/demo1')
def map_demo1():
    url = "https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/csv/file"
    r = requests.get(url)
    print(r)

    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    data_list = list(cr)

    # 使用 geocoder 取得特定住址的 GPS 座標
    location = geocoder.osm('新北市').latlng

    m = folium.Map(location=location, zoom_start=14)

    for item in data_list[1:]:
        try:
            name = item[1]
            area = item[4]
            total = item[2]
            n = item[3]
            lat = item[6]
            lng = item[7]
            if int(n)<5 and int(n)>0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='red', prefix='fa', icon='fa-bicycle')).add_to(m)
            elif int(n)==0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='black', prefix='fa', icon='fa-bicycle')).add_to(m)
            else:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='green', prefix='fa', icon='fa-bicycle')).add_to(m)
            
        except Exception as e:
            print(e.args)    

    m.save('map1.html')
                
    return send_file('./map1.html')



@app.route('/map/demo2')
def map_demo2():
    url = "https://raw.githubusercontent.com/maloyang/KH20221202_IoT_Data_Science/main/W01/bike_02_新北市.csv"
    r = requests.get(url)
    print(r)

    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    data_list = list(cr)

    # 使用 geocoder 取得特定住址的 GPS 座標
    location = geocoder.osm('新北市').latlng

    m = folium.Map(location=location, zoom_start=14)

    for item in data_list[1:]:
        try:
            name = item[1]
            area = item[4]
            total = item[2]
            n = item[3]
            lat = item[6]
            lng = item[7]
            if int(n)<5 and int(n)>0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='red', prefix='fa', icon='fa-bicycle')).add_to(m)
            elif int(n)==0:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='black', prefix='fa', icon='fa-bicycle')).add_to(m)
            else:
                folium.Marker([float(lat), float(lng)], tooltip=name+'<br>剩餘車輛:%s/%s' %(n,total),
                            icon=folium.Icon(color='green', prefix='fa', icon='fa-bicycle')).add_to(m)
            
        except Exception as e:
            print(e.args)    

    #m.save('/home/malocsu8107/mysite/map1.html')            
    #return send_file('/home/malocsu8107/mysite/map1.html')

    m.save('map1.html')            
    return send_file('./map1.html')


@app.route('/sql/gettest')
def sql_gettest():
    table_name = 'malo_khair_1210'
    sid = '左營國小'
    sql_cmd_str = "select * from %s where sid='%s'" %(table_name, sid)
    resultProxy=my_db.execute(sql_cmd_str)
    data = resultProxy.fetchall()
    print('-- data --')
    #print(data)
    data_list = []
    for item in data:
        print(item)
        data_list.append(dict(item))    

    return jsonify({'result':'OK', 'data':data_list})


@app.route('/sqlinner/create')
def sqlinner_create():
    mysql_db_url2 = 'mysql+pymysql://malocsu8107:my12345678sql@malocsu8107.mysql.pythonanywhere-services.com:3306/malocsu8107$mytest1'
    my_db2 = create_engine(mysql_db_url2)
    table_name = 'malo_test_1212'
    sql_cmd_str = "CREATE TABLE IF NOT EXISTS %s(dtime varchar(20) PRIMARY KEY, temp float)" %(table_name)
    resultProxy = my_db2.execute(sql_cmd_str)
            
    return jsonify({'result':'OK'})


@app.route('/sqlinner/upsert')
def sqlinner_upsert():
    mysql_db_url2 = 'mysql+pymysql://malocsu8107:my12345678sql@malocsu8107.mysql.pythonanywhere-services.com:3306/malocsu8107$mytest1'
    my_db2 = create_engine(mysql_db_url2)
    table_name = 'malo_test_1212'

    #upsert data
    dt1 = datetime.datetime.strptime('2022-12-01 08:00:00','%Y-%m-%d %H:%M:%S') #把時間字串轉為datetime物件
    for i in range(10):
        str_dt = (dt1+datetime.timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
        temp = random.randint(350, 375)/10
        #print(str_dt, temp)
        sql_cmd_str = "insert into %s (dtime, temp) values('%s', '%s')" %(table_name, str_dt, temp)
        sql_cmd_str = sql_cmd_str + (" ON DUPLICATE KEY UPDATE temp='%s'" %(temp))
        resultProxy=my_db2.execute(sql_cmd_str)
            
    return jsonify({'result':'OK'})


@app.route('/sqlinner/select')
def sqlinner_select():
    mysql_db_url2 = 'mysql+pymysql://malocsu8107:my12345678sql@malocsu8107.mysql.pythonanywhere-services.com:3306/malocsu8107$mytest1'
    my_db2 = create_engine(mysql_db_url2)
    table_name = 'malo_test_1212'

    sql_cmd_str = "select * from %s" %(table_name)
    resultProxy=my_db2.execute(sql_cmd_str)
    data = resultProxy.fetchall()
    print('-- data --')
    print(data)
    data_list = []
    for item in data:
        my_data = dict(item)
        data_list.append(my_data)

    return jsonify({'result':'OK', 'data':data_list})


@app.route('/api/temp', methods=['GET'])
def api_temp():
    mysql_db_url2 = 'mysql+pymysql://malocsu8107:my12345678sql@malocsu8107.mysql.pythonanywhere-services.com:3306/malocsu8107$mytest1'
    my_db2 = create_engine(mysql_db_url2)
    table_name = 'malo_test_1212'

    sql_cmd_str = "select * from %s" %(table_name)
    resultProxy=my_db2.execute(sql_cmd_str)
    data = resultProxy.fetchall()
    print('-- data --')
    print(data)
    data_list = []
    for item in data:
        my_data = dict(item)
        data_list.append(my_data)

    return jsonify({'result':'OK', 'data':data_list})



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8100)
