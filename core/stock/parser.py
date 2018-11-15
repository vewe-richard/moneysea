# coding=utf-8
import os
from globals import Globals
from fileparsers.financial import FinancialHistory

class Parser:
    def __init__(self, stockpath):
        self._stockpath = stockpath
        self.doparse()
        pass

    def doparse(self):
        items = os.path.basename(os.path.dirname(self._stockpath)).split("-")
        self._id = int(items[0])
        self._name = Globals.get_instance().sin.getname(self._id)

        self._fh = FinancialHistory(self._stockpath + "/finance")
        self._fh.doparse()

        self._latestfd = self._fh.getlatest()

        #最新季报净利润/每股收益 = 总股数
        self._totalstocks = self._latestfd.profit / self._latestfd.per_share_earnings

        #最近365天净利润 = 最新季报净利润 + 上一年年报净利润 - 上一年同季净利润
        #每股收益 = 最近365天净利润 / 总股数
        prev_fd = self._fh.getreport(self._latestfd.year - 1, self._latestfd.season) #上一年同季净利润
        yearProfit = self._latestfd.profit + self._fh.get_year_report(self._latestfd.year - 1).profit - prev_fd.profit
        self._pershareearnings = yearProfit / self._totalstocks
        pass

    def getpershareearnings(self):
        return self._pershareearnings

    def getid(self):
        return self._id

    def getname(self):
        return self._name


if __name__ == "__main__":
    psr = Parser("input/stocks/300230-ylgf/")

    print psr.getid()
    print psr.getname()
    print psr.getpershareearnings()
    pass
