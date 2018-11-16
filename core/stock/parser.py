# coding=utf-8
import os
from globals import Globals
from fileparsers.financial import FinancialHistory
from fileparsers.note import Note
from common import Common
from config import Config

class Parser:
    def __init__(self, stockpath):
        self._stockpath = stockpath
        self.adding = {"in report": None}

        self.doparse()
        pass

    def doparse(self):
        if self._stockpath[-1] != "/": 
            self._stockpath += "/"
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

        note = Note(os.path.dirname(self._stockpath) + "/note.xml")
        try:
            note.doparse()
            self._note = note._note
            self.adding["manual"] = note._adding
        except:
            self._note = None
            self.adding["manual"] = None

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
        average = (self._fh.get_year_report(end - 1).profit/startprofit) ** (1.0 / Config.CONTINUE_GROW_YEARS) - 1
        return (continued, average)

    def average_profit2_adding(self):
        end = self._latestfd.year
        start = self._latestfd.year - Config.CONTINUE_GROW_YEARS
        startprofit = self._fh.get_year_report(start - 1).profit2
        average = (self._fh.get_year_report(end - 1).profit2/startprofit) ** (1.0 / Config.CONTINUE_GROW_YEARS) - 1
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

    def forcast(self, earnings, price, title, adding):
        print title + ":%6.2f"%(adding)

        earnings2 = earnings * ((1 + adding)**2)
        price10 = earnings2*100 / 10  #对应10%收益的价格
        avg = ((price10 /price) ** (1.0 / 2)) - 1
        print "两年预期每股收益:%6.2f"%earnings2, "\t[10%", "Price]: %6.2f"%price10, "年均增长: %6.2f"%avg

        earnings5 = earnings * ((1 + adding)**5)
        price10 = earnings5*100 / 10
        avg = ((price10/price) ** (1.0 / 5)) - 1
        print "五年预期每股收益:%6.2f"%earnings5, "\t[10%", "Price]: %6.2f"%price10, "年均增长: %6.2f"%avg

        print ""
        pass

    def outputVerbose(self):
        earnings = self.getpershareearnings()
        price = Globals.get_instance().getstockprice(self.getid())
        print ""
        print self.getname(), "(", self.getid(), ")"
        print "Price:", price
        print "每股收益: %7.3f"%earnings, "\t折算利率:%6.2f"%(earnings/price),"\t区间[%15, %10, %5]:", "[%6.2f %6.2f %6.2f]"%(self._pricesRange[0], self._pricesRange[1], self._pricesRange[2])
        print "净资产收益率: %6.2f"%self._asset_adding2, "\t平均净资产收益率: %6.2f"%self._average_asset_adding2
        print "稳定增长:", self._continued[0], "\t\t365增长加快:", self._increase_fasten[0], "\t报告季增长加快:", self._increase_fasten[1]

        print ""
        self.forcast(earnings, price, "报告季增长", self.adding["in report"])
        self.forcast(earnings, price, "365增长", self.adding["adjacent 365"])
        self.forcast(earnings, price, "平均净利润增长", self._continued[1])

        self.forcast(earnings, price, "报告季扣非净利润增长", self.adding["profit2"])
        self.forcast(earnings, price, "平均扣非净利润增长", self.adding["average profit2"])
        self.forcast(earnings, price, "综合分析增长", self.adding["manual"])

        print self._note

    def outputSimple(self):
        print ""
        print ""
        print "%40s"%("flag:"), "稳定增长|365增长|报告季增长"
        title = "%9s,%7s,%8s,%6s,%8s,%7s,%5s,%7s,%8s,%8s" % ("stockname", "id", "earning", "price", "total", "asset%", "flag", "adding", "2Yprice", "5Yprice")
        print title
        n = self.getname()
        i = self.getid()
        e = self.getpershareearnings()
        p = Globals.get_instance().getstockprice(self.getid())
        t = Globals.get_instance().getstocktotal(self.getid())
        a = self._asset_adding2

        adding = self.getadding()

        earnings2 = e * ((1 + adding)**2)
        y2 = earnings2*100 / 10  #对应10%收益的价格

        earnings5 = e * ((1 + adding)**5)
        y5 = earnings5*100 / 10
        print "%9s,%8s,%8.2f,%6.2f,%8.0f,%7.2f,%5s,%7.2f,%8.2f,%8.2f" % (n, i, e, p, t, a, self.getFlag(), adding, y2, y5)

    def getFlag(self):
        a = ""
        for v in  (self._continued[0], self._increase_fasten[0], self._increase_fasten[1]):
            if v:
                a += "T"
            else:
                a += "F"
        return a



    def getadding(self):
        if self.adding["manual"] != None:
            return self.adding["manual"]



if __name__ == "__main__":
    psr = Parser("input/stocks/300230-ylgf/")
    psr.outputVerbose()
    psr.outputSimple()


    pass
