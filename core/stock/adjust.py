# coding=utf-8
import sys

from os import listdir
import os
from config import Config

from globals import Globals
from stock.parser import Parser


class Adjust:
    def __init__(self, n, p):
        self.n = n
        self.p = p

    def run(self):
        self.stocklists = {}

        for f in listdir(Config.STOCKS_PATH):
            fin = Config.STOCKS_PATH + "/" + f + "/finance"
            if not os.path.exists(fin):
                continue
            items = f.split("-")
            idx = items[1]

            psr = Parser(Config.STOCKS_PATH + "/" + f)
            if psr._pershareearnings < 0.01:
                continue

            q = Globals.get_instance().getstockprice3(idx)
            eq = psr._pershareearnings / q

            stock = {}
            stock["name"] = psr._name
            stock["earnings"] = psr._pershareearnings
            stock["q"] = q
            stock["eq"] = eq
            

            suitcount = 0
            for val in psr.adding:
                if val == "manual":
                    continue
                info = {}

                a = psr.adding[val]
                ref = (((1.0 + self.p)/(1 + a))**self.n)*self.p  # reference eq
                delta = ((psr._pershareearnings / ref) - q)/q

                info["a"] = a
                info["ref"] = ref
                info["delta"] = delta
                stock[val] = info
                if delta > 0.001:
                    suitcount += 1

            stock["count"] = suitcount
            self.stocklists[idx] = stock

        pass

    def stastics(self):
        counts = {}
        for adding in Config.ADDINGS:
            counts[adding] = 0

        total = 0
        for i in self.stocklists:
            item = self.stocklists[i]
            total += 1
#            print i, item["name"], item["earnings"], item["q"], item["eq"]
            for adding in Config.ADDINGS:
                val = item[adding]
                if val["delta"] > 0.001:
                    counts[adding] += 1


        print "==================== statistics ========================="
        print "total stocks with earnings > 0:", total
        for adding in Config.ADDINGS:
            print "adding type: %10s"%adding, "\t suitable ",  counts[adding], "percent", counts[adding] * 1.0 / total

        print ""
        for i in self.stocklists:
            item = self.stocklists[i]
            if item["count"] < 5:
                continue
            print i, item["name"], item["earnings"], item["q"], item["eq"], item["count"]
        pass

    def output(self):
        self.stastics()
        pass







