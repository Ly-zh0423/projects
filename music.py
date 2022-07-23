import os
import time
import json

dirname = os.path.split(os.path.abspath( __file__))
path = dirname[0] + "\package\\"
import sys
sys.path.append(path)
from easys import Easy as Fc

start = Fc()
start.pip_pack(name=["requests", "rich"])
import requests
from rich.console import Console as Cp

class QQ_Music:
    """
    获取并返回新的QQ音乐信息 :

        参数(加*号的为必填项) : 
            *  keyword : 要获取的歌曲关键词;

        函数 : 
            parser : 解析音乐url;
            combination : 拼接音乐url;
            song_datas_dic : 储存歌曲信息的字典;

        用法 :
            mc = QQ_Music("司南")
            mc.parser()
            mc.combination()
            mc.song_datas_dic()
            司南为要搜索的音乐关键词;
        
        注意 :
            keyword(关键词) : 可以为歌曲名称/歌手名称/歌词/歌曲名称+歌手名称(搜索更准确)
    """

    def __init__(self, keyword):
        """ 初始化 """
        self.num = 1
        self.page = "50"
        # 初始化自定义包
        self.Fc = Fc()
        self.Cp = Cp()
        self.keyword = keyword
        if self.keyword != "":
            self.parser()

    def parser(self):
        """ parser : 解析音乐url """
        #self.Cp.print("正在运行函数：parser", style="red")
        try:
            # one在这里是转dict必须输入的，指定转换几个
            #headers = dict(one=random.choice(self.requests_headers))
            head_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n="+self.page+"&w="+self.keyword
            #print(head_url)
            response = requests.get(head_url, headers=self.Fc.Agents()).text
            response = response.strip('callback()')
            #print(response)
            # 解析json
            #print(type(response))
            json_data = json.loads(response)
            #print(type(json_data))
            json_data1 = json_data['data']['song']['list']
            #print(json_data2)
            # 创造列表
            self.song_Name = []
            # 歌名
            self.song_Singer = []
            # 歌手
            self.song_AlbumName = []
            # 专辑
            self.AlbumId = []
            # 歌曲号，用于拼接歌手图片
            self.song_StrMediaMid = []
            # 拼接音乐连接时使用

            # 获取并添加值
            try:
                for data in json_data1:
                    self.song_Name.append(data['songname'])
                    self.song_Singer.append(data['singer'][0]['name'])
                    self.song_AlbumName.append(data['albumname'])
                    self.song_StrMediaMid.append(data['strMediaMid'])
                    self.AlbumId.append(data['albumid'])
                time.sleep(3)
                self.combination()
            except:
                self.Cp.print("数据获取失败！1", style="red")
                #self.Cp.print(self.song_Name, self.song_Singer, self.song_AlbumName, self.song_StrMediaMid)
        except:
            self.Cp.print("数据获取失败！2", style="red")

    def combination(self):
        """ combination : 拼接音乐url """
        #self.Cp.print("正在运行函数：combination", style="red")
        try:
            self.song_Url = []
            for song in range(0, len(self.song_StrMediaMid)):
                # 音乐json请求网页
                url2 = 'https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"358840384","songmid":["%s"],"songtype":[0],"uin":"1443481947","loginflag":1,"platform":"20"}},"comm":{"uin":"18585073516","format":"json","ct":24,"cv":0}}'
                # 格式化写入url2
                purl = url2 % self.song_StrMediaMid[song]
                #print(purl)
                resp = requests.get(purl, headers=self.Fc.Agents())
                # 对结果进行解码
                ret_json = resp.content.decode()
                # 转化为字典
                ret_dict = json.loads(ret_json)
                purl = ret_dict["req_0"]["data"]["midurlinfo"][0]["purl"]
                # 这是最终的歌曲url
                url = ret_dict["req_0"]["data"]["sip"]
                #print(url)
                song_url = url[1] + purl
                #self.Cp.print(song_url)
                if len(song_url) <= 217:
                    # 判断真假音乐播放地址
                    self.song_Url.append(song_url)
                else:
                    self.Cp.print("该音乐无法下载！", style="red")
        except:
            self.Cp.print("函数combiation运行失败！", style="red")
        time.sleep(3)
        self.song_datas_dic()

    def song_datas_dic(self):
        """ song_datas_dic : 储存歌曲信息的字典 """
        #self.Cp.print("正在运行函数：song_datas_dic", style="red")
        try:
            self.datas = []
            #print(self.song_Name, self.song_Singer, self.song_AlbumName, self.song_StrMediaMid, self.song_url_list)
            for number in range(len(self.song_StrMediaMid)):
                if self.song_Url[number] != "http://isure.stream.qqmusic.qq.com/":
                    self.song_datas = {
                        "song_name": self.song_Name[number],
                        "song_singer": self.song_Singer[number],
                        "song_AlbuName": self.song_AlbumName[number],
                        "song_url": self.song_Url[number],
                        "song_img": "http://imgcache.qq.com/music/photo/album_300/%i/300_albumpic_%i_0.jpg" % (self.AlbumId[number] % 100, self.AlbumId[number])
                    }
                    self.datas.append(self.song_datas)
                    self.Cp.print(self.song_datas)
            # return self.datas
        except:
            pass

if __name__ == "__main__":
    while True:
        keyword = str(input("请输入关键词："))
        QQ_Music(keyword=keyword)
        number = (self.datas/int(self.page))*100
        self.Cp.print("共计搜索:{} 条\n搜索结果:{} 条\n搜索丢失率{} %".format(int(self.page), len(self.datas), round(number)), style="blue")

        time.sleep(3)
    """
    mc = QQ_Music(keyword="司南")
    mc.parser()
    mc.combination()
    mc.song_datas_dic()
    """
"""
https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"7208009084","songmid":"0040rS0Y2eItVE","songtype":[0],"uin":"2883","loginflag":1,"platform":"20"}}}
http://dl.stream.qqmusic.qq.com/C400001U2GJO2hSzQW.m4a?guid=5080691353&vkey=F27182982F4EB58E809420D33AE345A9D0C5037797A25D62BD8B26732B8BF81C2E511ECA62DAF5489AB7348CA28FDBF95DFD7C5A1F6275A1&uin=2843937603&fromtag=66
"""





