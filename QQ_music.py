import os
import time
import json

dirname = os.path.split(os.path.abspath( __file__))
path = dirname[0] + "\package\\"
import sys
sys.path.append(path)
from 副本 import Easy as Fc

import requests
from rich.console import Console as Cp

class Q_Music:
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
        # 初始化自定义包
        self.Fc = Fc()
        self.Cp = Cp()
        # 歌曲关键词
        self.keyword = keyword
        # 查找页数
        self.page = 1
        # 每页最大显示量
        self.page_num = 10
        if self.keyword != "":
            self.parser()
        

    def buildSearchContent(self, keyword, page_num, page):
        """ buildSearchContent : 建立搜索内容(请求头) """
        return {
        "comm": {"ct": "19", "cv": "1845"},
        "music.search.SearchCgiService": {
        "method": "DoSearchForQQMusicDesktop",
        "module": "music.search.SearchCgiService",
        "param": {"query": keyword, "num_per_page": page_num, "page_num": page}
        }
    }

    def getHead(self):
        """ getHead : 获取请求头 """
        return {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        "content-type": "application/json; charset=UTF-8",
        "referer": "https://y.qq.com/portal/profile.html"
    }

    self.sess = requests.Session()

    def parser(self):
        """ parser : 解析音乐url """
        self.Cp.print("正在运行函数：parser", style="red")
        try:
            # 请求链接
            url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
            # base data content from qqmusic pc-client-apps
            sess = requests.Session()
            data = self.buildSearchContent(self.keyword, self.page_num, self.page)
            data = json.dumps(data, ensure_ascii=False)
            data = data.encode("utf-8")
            res = sess.post(url, data, headers=self.getHead())
            jsons = res.json()
            
            # 解析json数据
            # 开始解析QQ音乐的搜索结果
            json_data = jsons["music.search.SearchCgiService"]["data"]["body"]
            # 歌曲详细信息
            json_data1 = json_data["song"]["list"]
            # 歌手详细信息
            json_data2 = json_data["zhida"]["list"]
            

            # 创建列表
            self.song_datas_dic = []
            self.singer_datas_dic = []

            # 获取并添加值
            try:
                # 添加歌曲详细信息
                # album name 歌曲名称
                # singer name 歌手名称
                # album id 歌曲 id
                # album mid 歌曲 mid
                # file media_mid 音频 mid
                # file size_128mp3 歌曲mp3音质大小

                for data1 in json_data1:
                    self.song_datas_dic.append({
                        "song_Name": data1["album"]["name"],
                        "song_Singer": data1["singer"][0]["name"],
                        "song_AlbumId": data1["album"]["id"],
                        "song_AlbumMid": data1["album"]["mid"],
                        "song_MediaMid": data1["file"]["media_mid"],
                        "song_Size": str(round(data1["file"]["size_128mp3"]/(1024*1024), 3))+"Mb",
                        #"song_Url": self.combination(data1["album"]["name"], data1["album"]["mid"], data1["file"]["media_mid"]),
                    })
                # 添加歌手详细信息
                # extra_desc 歌手粉丝总数
                # mid 歌手 mid
                # id 歌手 id
                # Desciption 歌手描述
                # title 歌手名称
            
                """for data2 in json_data2:
                    self.singer_datas_dic.append({
                        "Extra_desc": data2["custom_info"]["extra_desc"],
                        "Mid": data2["custom_info"]["mid"],
                        "Id": data2["id"],
                        "Desciption": data2["desciption"],
                        "Pic": data2["pic"],
                        "Title": data2["title"],
                        })"""
            except:
                self.Cp.print("音乐数据获取失败！", style="blue")
            self.Cp.print(self.song_datas_dic)
        except:
            self.Cp.print("json数据获取失败!", style="red")

    def getQQServersCallback(url, method=0, data={}):
        mqq_ = ""
        mkey_ = ""
        data1 = json.dumps(data, ensure_ascii=False)
        head = {
            'referer': 'https://y.qq.com/portal/profile.html',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': f'qqmusic_key={mkey_};qqmusic_uin={mqq_};',
            'content-type': 'application/json; charset=utf-8'
        }
        if method == 0:
            data2 = self.sess.get(url, headers=head)
        else:
            data2 = self.sess.post(url, data1, headers=head)
        return data2

    def parseSectionByNotFound(self, song_Name, song_Mid):
        """ parseSectionByNotFound : 当解析失败时用此函数获取vkey """
        data = getQQServersCallback('https://u.y.qq.com/cgi-bin/musicu.fcg', 1, {"comm": {"ct": "19", "cv": "1777"}, "queryvkey": {"method": "CgiGetVkey", "module": "vkey.GetVkeyServer",                 "param": {
        "uin": "",
        "guid": "QMD50",
        "referer": "y.qq.com",
        "songtype": [1],
        "filename": [song_name], "songmid": [song_mid]
        }}})
        data = data.json()
        vkey = data['queryvkey']['data']['midurlinfo'][0]['purl']
        print(vkey)

    def getMusicFileName(code, mid, format): 
        """ getMusicFileName : 获取音乐文件名称 """
        return f'{code}{mid}.{format}'

    def parser_get_url(self, song_Name, song_Mid, song_MediaMid):
        """ parser_get_url : 获取/解析音乐链接 """
        file = getMusicFileName(it['prefix'], it['mid'], it['extra'])
    
    """
    def song_datas_dic(self):
        "" song_datas_dic : 储存歌曲信息的字典 ""
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
            time.sleep(15)
            number = (1-len(self.datas)/int(self.page))*100
            self.Cp.print("共计搜索: {} 条\n搜索结果: {} 条\n搜索丢失率: {} %".format(int(self.page), len(self.datas), int(round(number, 4))), style="blue")
            # return self.datas
        except:
            pass"""

if __name__ == "__main__":
    keyword = "司南"#str(input("请输入关键词："))
    Q_Music(keyword=keyword)

    """
    mc = QQ_Music(keyword="司南")
    mc.parser()
    mc.combination()
    mc.song_datas_dic()
    """
"""
https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"7208009084","song_mid":"0040rS0Y2eItVE","songtype":[0],"uin":"2883","loginflag":1,"platform":"20"}}}
http://dl.stream.qqmusic.qq.com/C400001U2GJO2hSzQW.m4a?guid=5080691353&vkey=F27182982F4EB58E809420D33AE345A9D0C5037797A25D62BD8B26732B8BF81C2E511ECA62DAF5489AB7348CA28FDBF95DFD7C5A1F6275A1&uin=2843937603&fromtag=66
"""





