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

from globals import Globals
from stock.parser import Parser


class EarningAdding:
    def __init__(self):
        pass

    def run(self):
        ax = []
        ay = []

        for f in listdir(Config.STOCKS_PATH):
            fin = Config.STOCKS_PATH + "/" + f + "/finance"
            if not os.path.exists(fin):
                continue
            items = f.split("-")

            psr = Parser(Config.STOCKS_PATH + "/" + f)

            cox = psr._pershareearnings / Globals.get_instance().getstockprice3(items[1])
#            adding = psr._continued[1]
#            adding = psr.adding["adjacent 365"]
#            adding = psr.adding["profit2"]
            adding = psr.adding["average profit2"]
#            adding = psr.adding["in report"]

            print ""
            print items[1], Globals.get_instance().getstockprice3(items[1]), psr._pershareearnings, adding

            if adding > 1.2:
                adding = 1.0
            if cox > 0.20:
                cox = 0.2

            if adding < 0.0000001:
                continue
            if cox < 0.00001:
                continue

            ax.append(adding)
            ay.append(cox)

        print ax
        print ay

        nx = np.array(ax)
        ny = np.array(ay)
        plt.scatter(nx, ny, color='blue')

        n = 5 
        p = 0.10
        ax = []
        ay = []
        for i in range(0, 20):
            x = i / 20.0
            y = (((1.0 + p)/(1 + x))**n)*p
            if y > 0.2:
                print "out of range:", x, y
                y = 0.2
            ax.append(x)
            ay.append(y)

        nx = np.array(ax)
        ny = np.array(ay)
        plt.scatter(nx, ny, color='red')
        plt.plot(nx, ny, color='red', linewidth=4)
#        plt.plot(nx, regr.predict(nx.reshape(-1,1)), color='red', linewidth=4)

        plt.show()
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
