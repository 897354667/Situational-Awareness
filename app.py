# -*- coding:utf-8 -*-
from threading import Thread

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from admin import user,ipanalyse,sshanalyse,networkanalyse,processanalyse
from charts import apacheCharts,earthMapCharts,sshCharts,networkCharts,processCharts,attackeventCharts
from charts.manage import ip_manageCharts
from admin.manage import ip_manage


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


ncap = Thread(target=networkanalyse.networkanalyse)
ncap.start()


# 登录面板
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        info=user.check(str(username),str(password))
        if info=='登录成功':
            return redirect(url_for('index'))
        else:
            return render_template('login.html', login_info='账号或密码错误')
    else:
        return render_template('login.html')


#ip管理
@app.route('/ip_manage',methods=['GET','POST'])
def ip_manage():

    if request.method == 'POST':
        search = request.form['search']
        addwhite = request.form['addwhite']
    else:
        search=0
        addwhite=0

    if search:
        length, ip_list, country_name, country_specificname, city_name, time = ip_manageCharts.ip_searchCharts(search)
    else:
        length,ip_list,country_name,country_specificname,city_name,time=ip_manageCharts.selectalllistCharts()
    ipcountry_pie = ip_manageCharts.selectby_countryCharts()
    return render_template('manage/ipmanage.html',
                           ipcountry_pie=ipcountry_pie.render_embed(),
                           length=length,
                           ip_list=ip_list,
                           country_name=country_name,
                           country_specificname=country_specificname,
                           city_name=city_name,
                           time=time,
                           addwhite=addwhite,
                           )



#原始数据
@app.route('/get_raw_data',methods=['GET','POST'])
def get_raw_data():
    ip = request.form['ip']
    return ip

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

#系统设置
@app.route('/config',methods=['GET'])
def config():
    return 'dd'

#面板首页
@app.route('/index',methods=['GET','POST'])
def index():
    #图表绘制
    apachecharts=apacheCharts.apachePieCharts()
    apache_id = apachecharts._chart_id
    earthmapcharts=earthMapCharts.earthMap()
    earthmap_id=earthmapcharts._chart_id
    sshcharts,risk_index=sshCharts.sshPieCharts()
    sshcharts_id=sshcharts._chart_id
    networkcharts=networkCharts.networkcharts()#饼状图
    networkcharts_id=networkcharts.chart_id
    streamcharts=networkCharts.streamcharts()
    processcharts=processCharts.processCharts()
    ip_list,time_list,type_list=attackeventCharts.selectevent()
    length=len(ip_list)
    return render_template('base.html',
                           apachecharts=apachecharts.render_embed(),
                           apache_id=apache_id,
                           earthmapcharts=earthmapcharts.render_embed(),
                           earthmap_id=earthmap_id,
                           sshcharts=sshcharts.render_embed(),
                           sshcharts_id=sshcharts_id,
                           # gauge=gauge.render_embed(),
                           networkcharts=networkcharts.render_embed(),
                           networkcharts_id=networkcharts_id,
                           streamcharts=streamcharts.render_embed(),
                           processcharts=processcharts.render_embed(),
                           risk_index=risk_index,
                           ip_list=ip_list,
                           time_list=time_list,
                           type_list=type_list,
                           length=length,
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
