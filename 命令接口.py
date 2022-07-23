#导入命令接口所需库
import argparse

from music import QQ_Music as Qm

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
        parser = argparse.ArgumentParser(description="命令提示(加*号的为必选参数, 其余为选参)")
        #default为此参数的默认值

        parser.add_argument("-I", "--image", default="n", help=" : 是否下载音乐封面图 (y/n, 默认为n)")
        parser.add_argument("-K", "--keyword", help="* : 输入关键词[可输入歌名/歌手/歌词/歌名+歌手 (这样搜索更加准确)]")
        parser.add_argument("-M", "--mv", default="n", help=" : 是否下载音乐 MV (y/n, 默认为n)")
        parser.add_argument("-L", "--lyric", default="n", help=" : 是否下载歌词 (y/n, 默认为n)")
        parser.add_argument("-Su", "--song-url", default="n", help="是否输出音乐链接 (y/n, 默认为n)")
        parser.add_argument("-Ui", "--ui", default="n", help="是否启用ui面板 (y/n, 默认为n)")

        args = parser.parse_args()
        self.image = args.image
        self.keyword = args.keyword
        self.mv = args.mv
        self.lyric = args.lyric   
        self.song_url = args.song_url
        self.ui = args.ui
        
        self.parsers()

    def parsers(self):
        """ parsers : 解析命令 """
        #self.Cp.print(self.image, self.keyword, self.mv, self.lyric, self.song_url, self.ui)
        if self.keyword == None:
            self.Cp.print("您已进入终端控制台!", style="red")
            keyword = str(input("请输入关键词>>> "))
            self.Cp.print("正在搜索中,请耐心等待...", style="red")
            Qm(keyword)
        else:
            self.Cp.print("正在搜索中,请耐心等待...", style="red")
            Qm(self.keyword )

if __name__ == "__main__":
    start = Argparses()
    start.commands()