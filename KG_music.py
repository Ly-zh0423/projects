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

class K_Music:
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
        self.keyword = keyword
        if self.keyword != "":
            self.parser()

    def parser(self):
        """ parser : 解析音乐url """
        try:
            head_url = "https://songsearch.kugou.com/song_search_v2?keyword={}page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1580194546709".format(self.keyword)
            response = requests.get(head_url, headers=self.Fc.Agents()).text
            #解析json数据
            json_data = json.loads(response)
            json_data1 = json_data["data"]["lists"]
            #self.Cp.print(json_data1)
            
            # 创建列表
            self.song_Name = []
            # 歌名
            self.song_Singer = []
            # 歌手
            self.song_AlbumName = []
            # 专辑
            self.song_filehash = []
            # 拼接音乐连接时使用
            self.song_AlbumId = []
            # 歌曲号，用于拼接歌手图片
            
            # 获取并添加值
            try:
                for data in json_data1:
                    self.song_Name.append(data['SongName'].replace("<em>", "").replace("</em>", ""))
                    self.song_Singer.append(data['SingerName'].replace("<em>", "").replace("</em>", ""))
                    self.song_AlbumName.append(data['AlbumName'].replace("<em>", "").replace("</em>", ""))
                    self.song_filehash.append(data['FileHash'])
                    self.song_AlbumId.append(data['AlbumID'])
                self.combination()
            except:
                self.Cp.print("数据获取失败！1", style="red")
            #self.Cp.print(self.song_Name, self.song_Singer, self.song_AlbumName, self.song_filehash, self.song_AlbumId)
        except:
            self.Cp.print("数据获取失败！2", style="red")

    def combination(self):
        """ combination : 拼接音乐url """
        #self.Cp.print("正在运行函数：combination", style="red")
        #try:
        self.song_Url = []
        #设置cookies，否则请求会无数据
        cookies_dict = {}
        cookies1 = 'kg_mid=b434c13fcd475da311e141a0cf532557; _WCMID=16477e145e53a4a7e38ece94; kg_dfid=1aJRd418KcGl0dnFZB3ucZDk; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1582544353; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e'
        cookies_list = cookies1.replace(' ', '').split(';')
        for str1 in cookies_list:
            key, values = str1.split('=', 1)
            cookies_dict[key] = values
        self.cookies = cookies_dict
        
        #拼接数据
        for num in range(len(self.song_filehash)):
            if len(self.song_filehash[num]) > 0 and len(self.song_AlbumId[num]) > 0:
                end_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}&album_id={}'.format(self.song_filehash[num], self.song_AlbumId[num])
                url_text = requests.get(end_url, headers=self.Fc.Agents(), cookies=self.cookies).content
                #解析json
                print(url_text.decode("unicode_escape"))
                """url_json = json.loads(json.dumps(url_text))
                self.Cp.print(url_json["data"]["avatar"])
                self.Cp.print(url_json["data"]["play_backup_url"])"""

if __name__ == "__main__":
    keyword = "司南"#str(input("请输入关键词："))
    start = K_Music(keyword)