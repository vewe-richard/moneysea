# coding=utf-8
import os
from globals import Globals
from fileparsers.financial import FinancialHistory
from common import Common
from config import Config

class Parser:
    def __init__(self, stockpath):
        self._stockpath = stockpath
        self.adding = {"in report": None}

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

        #每股收益 = 最近365天净利润 / 总股数
        self._pershareearnings = self.get365Profit(self._latestfd)/ self._totalstocks

        #[15% ~ 10% ~ 5%]区间收益
        self._pricesRange = Common().pricesRange(self._pershareearnings)

        #parse adding ...
        #报告季增长
        self.adding["in report"] = self._latestfd.profit_adding / 100
        #最近两个365增长，即最新季度往前推一年，和更早的一年，之间净利润的增长
        prev_fd = self._fh.getreport(self._latestfd.year - 1, self._latestfd.season) #上一年同季净利润
        prev_profit365 = self.get365Profit(prev_fd)
        profit365 = self.get365Profit(self._latestfd)
        adding = (profit365 - prev_profit365) / prev_profit365
        self.adding["adjacent 365"] = adding
        #持续增长分析
        self._continued = self.continueParsing()
        #增长加快评级
        self._increase_fasten = self.increaseAdding()
        #净资产收益率 
        self._asset_adding2 = self._pershareearnings/self._latestfd.per_share_asset
        #净资产收益率近年平均值
        self._average_asset_adding2 = self.getAverageAssetAdding2()
        #扣非净利率增长
        self.adding["profit2"] = self._latestfd.profit2_adding / 100
        #扣非净利率平均增长
        self.adding["average profit2"] = self.average_profit2_adding()

    def increaseAdding(self):
        return (self.adding["adjacent 365"] >= self._continued[1], self.adding["in report"] >= self.adding["adjacent 365"])

    def continueParsing(self):
        continued = True
        end = self._latestfd.year
        start = self._latestfd.year - Config.CONTINUE_GROW_YEARS
        for y in range(start, end):
            old = self._fh.get_year_report(y - 1)
            val = self._fh.get_year_report(y)
            adding = (val.profit - old.profit)/old.profit
            if adding < Config.ALLOW_MAX_LOSS:
                print y, "grow is unsatisfied, it's ", adding
                continued = False
        startprofit = self._fh.get_year_report(start - 1).profit
        average = ((self._fh.get_year_report(end - 1).profit - startprofit)/startprofit) ** (1.0 / Config.CONTINUE_GROW_YEARS) - 1
        return (continued, average)

    def average_profit2_adding(self):
        end = self._latestfd.year
        start = self._latestfd.year - Config.CONTINUE_GROW_YEARS
        startprofit = self._fh.get_year_report(start - 1).profit2
        print startprofit, self._fh.get_year_report(end - 1).profit2, Config.CONTINUE_GROW_YEARS
        average = ((self._fh.get_year_report(end - 1).profit2 - startprofit)/startprofit) ** (1.0 / Config.CONTINUE_GROW_YEARS) - 1
        return average

        #最近365天净利润 = 最新季报净利润 + 上一年年报净利润 - 上一年同季净利润
    def get365Profit(self, fd):
        prev_fd = self._fh.getreport(fd.year - 1, fd.season) #上一年同季净利润
        profit365 = fd.profit + self._fh.get_year_report(fd.year - 1).profit - prev_fd.profit
        return profit365

    def getAverageAssetAdding2(self):
        end = self._latestfd.year
        start = self._latestfd.year - Config.CONTINUE_GROW_YEARS
        total = 0
        for y in range(start, end):
            val = self._fh.get_year_report(y)
            total += val.asset_adding2
        return total / 6 / 100

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
    print psr._pricesRange
    print psr.adding
    print psr._continued
    print psr._increase_fasten, "(年度增长加快，季度增长加快)"
    print psr._asset_adding2
    print psr._average_asset_adding2
    pass
