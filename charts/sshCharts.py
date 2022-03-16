import json

from pyecharts import Line,Pie,Grid
from model.ssh import Ssh
import admin.ipanalyse as ipanalyse

def selectssh():
    ssh=Ssh()
    ssh_list = ssh.query.all()
    ip_list=list()
    num_list=list()
    for i in ssh_list:
        ip_list.append(i.ip)
        num_list.append(i.num)
    return ip_list,num_list

# def sshLineCharts():#ssh攻击统计折线图
#     ip_list,num_list=selectssh()
#     ssh_line=Line("Ssh爆破攻击趋势图")
#     ssh_line.add('Ssh爆破攻击趋势',ip_list,num_list,is_show=True)
#     # ssh_line.render()
#     ssh_line.chart_id="ssh_line"
#     ssh_line.render()
#     # return ssh_line

def sshPieCharts():
    ip_list, num_list = selectssh()
    grid = Grid(width="100%", height="100%")
    ssh_pie=Pie()
    ssh_pie.add("ssh爆破统计", ip_list, num_list, radius=[28, 38], label_text_color=None,
            legend_orient='vertical', center=[15, 25], is_legend_show=False, is_toolbox_show=False,
            is_label_show=False,)
    # ssh_pie.render()
    ssh_sum=0
    for i in num_list:
        ssh_sum+=int(i)
    # print(ssh_sum)
    with open('./output/analyse/network/flowStatistics.txt', 'r') as fp:
        streams = json.load(fp)
        val = list(streams.values())
        stream_in=0
        for v in val:
            stream_in+=v[0]
        # print(stream_in)
    risk=ssh_sum/stream_in
    risk_index='{:.0%}'.format(risk)
    return ssh_pie,risk_index
# sshPieCharts()