# -*- coding:utf-8 -*-
from threading import Thread

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from admin import user,ipanalyse,sshanalyse,networkanalysedemo
from charts import apacheCharts,earthMapCharts,sshCharts,networkCharts

# 建立flask对象
app = Flask(__name__)
# 载入配置文件
app.config.from_pyfile('config.py')
# 创建数据库对象
db = SQLAlchemy(app)

# #面板首页
# @app.route('/',methods=['GET','POST'])
# def index():
#     return 'Hello World!'


netcap = networkanalysedemo.netCapture()
ncap = Thread(target=netcap.capture)
ncap.start()


#登录面板
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        info=user.check(str(username),str(password))
        return info
    else:
        return render_template('login.html')

#分析ip，结果存入数据库
@app.route('/ip',methods=['GET'])
def localbyip():
    ip=request.args.get('ip')
    ipanalyse.seperate_ip(ip)
    return 'ip存入'

@app.route('/ssh',methods=['GET'])
def ssh():
    sshanalyse.analyseByfile()
    return 'ssh存入'

@app.route('/apache',methods=['GET'])
def apache():
    sshanalyse.analyseByfile()
    return 'apache存入'

#面板首页
@app.route('/',methods=['GET','POST'])
def index():
    #图表绘制
    apachecharts=apacheCharts.apachePieCharts()
    apache_id = apachecharts._chart_id
    earthmapcharts=earthMapCharts.earthMap()
    earthmap_id=earthmapcharts._chart_id
    sshcharts=sshCharts.sshLineCharts()
    sshcharts_id=sshcharts._chart_id
    # print(sshcharts_id)
    # stream_chart = networkCharts.stream_status(streams)
    # stream_id = stream_chart._chart_id

    return render_template('base.html',
                           apachecharts=apachecharts.render_embed(),
                           apache_id=apache_id,
                           earthmapcharts=earthmapcharts.render_embed(),
                           earthmap_id=earthmap_id,
                           sshcharts=sshcharts.render_embed(),
                           sshcharts_id=sshcharts_id,)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
