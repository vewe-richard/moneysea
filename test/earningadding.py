# coding=utf-8
import sys

from fileparsers.financial import FinancialHistory
from os import listdir
import os
from config import Config

from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np

import urllib2


class EarningAdding:
    def __init__(self):
        pass

    def run(self):
        for f in listdir(Config.STOCKS_PATH):
            fin = Config.STOCKS_PATH + "/" + f + "/finance"
            if not os.path.exists(fin):
                continue
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

    ea = EarningAdding()
#    ea.run()
    ea.test()
