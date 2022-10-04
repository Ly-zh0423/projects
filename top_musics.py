import re
import sys
import json
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"\\packages\\")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"\\packages\\")
from easy_pack import Easy as Fc
from color_print import Color as Cp


start = easys.easy()

class top_music():
    def __init__(self):
        self.headers = start.Agents()
        self.QQ_url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?page=detail&tpl=macv4&type=top&topid=26&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
        self.KG_url = "https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank"

    def QQ_tops(self):
        QQ_song_name = []
        QQ_singer = []
        QQ_song_list = []
        html_text = requests.get(self.QQ_url, headers=self.headers).text
        #解析json数据
        html_json = json.loads(html_text)
        song_data = html_json["songlist"]
        for data in range(len(song_data)):
            data = song_data[data]
            for keyword in data:
                if keyword == "data":
                    QQ_song_name.append(data[keyword]["songname"])
                    QQ_singer.append(data[keyword]["singer"][0]["name"])
        for number in range(100):
            song_list = QQ_singer[number] + "-" + QQ_song_name[number]
            QQ_song_list.append(song_list)
        return QQ_song_list

    def KG_tops(self):
        KG_song_list = []
        for page in range(6):
            html_text = requests.get(self.KG_url.format(page), headers = self.headers).text
            singer_song = re.findall(r'<a .*? title="(.*?)">.*?</a>', str(html_text))
            #去除列表重复项
            song_data = np.unique(singer_song)
            for datas in song_data:
                data = datas.strip('"播放全部" data-active="play" data-index=""  hidefocus="true" "下载" "分享"')
                KG_song_list.append(data)
        return KG_song_list

    def parser(self, QQ_song_list, KG_song_list):
        #查找相同内容
        lists = []
        for QQ_list in QQ_song_list:
            for KG_list in KG_song_list:
                if QQ_list == KG_list:
                    lists.append(KG_list)
                else:
                    pass

run = top_music()
QQ = run.QQ_tops()
KG = run.KG_tops()
run.parser(QQ, KG)