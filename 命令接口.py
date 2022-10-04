import os
import sys
dirname = os.path.split(os.path.abspath( __file__))
path = dirname[0] + "\package\\"
sys.path.append(path)
from easys import Easy as Fc
run = Fc()
run.pip_pack(["argparse", "requests", "rich"])
import argparse

from QQ_music import Q_Music as Qm

#着色输出所需库
from rich.console import Console as Cp

class Argparses:
    """
    Python命令终端接口函数;
    """
    def __init__(self, **kwargs):
        """ 初始化 """
        self.Cp = Cp()

    def commands(self):
        """ commands : 解析命令行接口 """
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="命令提示(加*号的为必选参数, 其余为选参)")
        #default为此参数的默认值
        parser.add_argument("-K", "--keyword", help="* : 输入关键词[可输入歌名/歌手/歌词/歌名+歌手 (这样搜索更加准确)]")

        parser.add_argument("-A", "--api", choices=["qq", "kg"], default="qq", help=" : 选择接口(QQ/酷狗, 默认为QQ音乐)")
        #parser.add_argument("-I", "--image", choices=["y", "n"], default="n", help=" : 下载音乐封面图 (y/n, 默认为n)")
        #parser.add_argument("-M", "--mv", choices=["y", "n"], default="n", help=" : 下载音乐 MV (y/n, 默认为n)")
        #parser.add_argument("-L", "--lyric", choices=["y", "n"], default="n", help=" : 下载歌词 (y/n, 默认为n)")
        #parser.add_argument("-Su", "--song-url", choices=["y", "n"], default="n", help=" : 输出音乐链接 (y/n, 默认为n)")
        #parser.add_argument("-Ui", "--ui", default="n", help="是否启用ui面板 (y/n, 默认为n\n注意: 此项只可单独使用!)")

        args = parser.parse_args()
        self.api = args.api
        self.image = args.image
        self.keyword = args.keyword
        self.mv = args.mv
        self.lyric = args.lyric   
        self.song_url = args.song_url
        #self.ui = args.ui
        
        self.parsers()

    def parsers(self):
        """ parsers : 解析命令 """
        #self.Cp.print(self.image, self.keyword, self.mv, self.lyric, self.song_url, self.ui)
        if self.keyword == None:
            self.Cp.print("您已进入终端控制台, 当前api为: {}".format(self.api), style="red")
            keyword = str(input("请输入关键词>>> "))
            self.Cp.print("正在搜索中,请耐心等待...", style="red")
            if self.api == "qq":
                Qm(keyword)
            elif self.api == "kg":
                self.Cp.print("酷狗搜索", style="red")
            else:
                self.Cp.print("搜索跳过", style="red")
        else:
            self.Cp.print("当前api为: {}\n正在搜索中,请耐心等待...".format(self.api), style="red")
            if self.api == "qq":
                Qm(self.keyword)
            elif self.api == "kg":
                self.Cp.print("酷狗搜索", style="red")
            else:
                self.Cp.print("搜索跳过", style="red")

if __name__ == "__main__":
    start = Argparses()
    start.commands()