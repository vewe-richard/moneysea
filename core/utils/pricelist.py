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

    def getids(self, filepath, tag):
        mylist = []
        with open(filepath) as f:
            for line in f:
                items = line.split(")")
                for item in items:
                    ns = item.split("(")
                    if len(ns) == 2:
                        mylist.append(tag + ns[1])
        return mylist

    def run(self):
        count = 0
        mylist = ""
        self.plist = {}
        for item in self.getids(Config.STOCK_ID_NAME_MAP_SHA, "sh") + self.getids(Config.STOCK_ID_NAME_MAP_SZ, "sz") + self.getids(Config.STOCK_ID_NAME_MAP_OPEN, "sz"):
            mylist += item + ","
            count += 1
            if count == 3:
                self.request(mylist)
                count = 0
                mylist = ""
        if count > 0:
            self.request(mylist)

        json.dump(self.plist, open(Config.OUTPUT_PRICELIST,'w'))

    def request(self, mylist):
        myurl='http://hq.sinajs.cn/list=' + mylist

        req = urllib2.Request(url = myurl)
        res = urllib2.urlopen(req)
        res = res.read()
        lines = res.split("\n")
        for line in lines:
            vals = line.split(",")
            if len(vals) < 2:
                continue
            if len(vals) < 20:
                print line
                print "Unknown response on " + mylist
                continue
            idx = vals[0][13:19]
            price = float(vals[2])
            self.plist[idx] = price

    def run3(self):

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
        myurl='http://hq.sinajs.cn/list=sh600097,sh601003,sh601001,'  #目标网址
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
#    pl.run()
#    pl.test()
    pl.run2()
