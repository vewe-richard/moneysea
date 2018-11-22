# coding=utf-8
import sys

from os import listdir
import os
from config import Config
from globals import Globals
import json

import urllib2

class PriceList:
    def __init__(self):
        pass

    def run(self):

        myurl='http://hq.sinajs.cn/list='

        plist = {}
        for f in listdir(Config.STOCKS_PATH):
            fin = Config.STOCKS_PATH + "/" + f + "/finance"
            if not os.path.exists(fin):
                continue
            items = f.split("-")
            idx = int(items[1])
            name = Globals.get_instance().sin.getname(idx)
            if idx >= 600000:
                idy = "sh" + items[1]
            else:
                idy = "sz" + items[1]

            nurl = myurl + idy

            try:
                req = urllib2.Request(url = nurl)
                res = urllib2.urlopen(req)
                res = res.read()
                vals = res.split(",")

                price = float(vals[2])
            except:
                continue

            plist[items[1]] = price
        json.dump(plist, open(Config.OUTPUT_PRICELIST,'w'))
        pass

    def test(self):
        myurl='http://hq.sinajs.cn/list=sh600097'  #目标网址
        req = urllib2.Request(url = myurl)
        res = urllib2.urlopen(req)
        res = res.read()
        print(res)

        pass


if __name__ == "__main__":
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')

    pl = PriceList()
    pl.run()
#    pl.test()
