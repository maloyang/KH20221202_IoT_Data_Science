import csv
from sqlalchemy import create_engine

mysql_db_url = 'mysql+pymysql://root:ixnqjmysql@209.97.161.199:43306/KH20221202_IoT_Data_Science'
my_db = create_engine(mysql_db_url)

table_name = 'malo_khair_1210'

# 找出某個站的資料, 並排序: where, order
sid = '前鎮國小'
sql_cmd_str = "select * from %s where sid='%s' order by dtime ASC" %(table_name, sid)
resultProxy=my_db.execute(sql_cmd_str)
data = resultProxy.fetchall()
print('-- data --')
for item in data:
    print(dict(item))
    
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
