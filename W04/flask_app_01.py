
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import requests

# set timezone
os.environ["TZ"] = "Asia/Taipei"
time.tzset()

app = Flask(__name__)

#mysql_db_url = 'mysql+pymysql://root:password@206.189.86.205:32769/testdb'
mysql_db_url = 'mysql+pymysql://malocsu8107:ji3m/4mysqldb@malocsu8107.mysql.pythonanywhere-services.com/malocsu8107$mytest1'
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


@app.route('/

##==== MySQL Test
table_name = 'malo_test0927'

@app.route('/mysql/create')
def mysql_create():
    sql_cmd_str = "CREATE TABLE IF NOT EXISTS %s(dtime varchar(20) PRIMARY KEY, temp float)" %(table_name)
    resultProxy = my_db.execute(sql_cmd_str)
    return str(resultProxy.__dict__)


@app.route('/mysql/insert')
def mysql_insert():
    dt_now = datetime.datetime.now()
    str_dt = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    temp = random.randint(350, 375)/10
    sql_cmd_str = "insert into %s (dtime, temp) values('%s', '%s')" %(table_name, str_dt, temp)
    resultProxy=my_db.execute(sql_cmd_str)
    print(resultProxy)
    return str(resultProxy.__dict__)

@app.route('/mysql/select/all')
def mysql_select_all():
    sql_cmd_str = "select * from %s ACS" %(table_name)
    resultProxy=my_db.execute(sql_cmd_str)
    data = resultProxy.fetchall()
    print('-- data --')
    print(data)
    return 'data: %s' %(data)



