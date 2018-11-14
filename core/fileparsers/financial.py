# coding=utf-8
# file source: On Ubuntu, using chromium to open 同花顺--永利股份，select 财务指标，按报告期
# Provide: 
# Verify: every season, 净资产收益率-摊薄 = 每股收益/每股净资产

from baseparser import BaseParser
import datetime

class FcData:
    def __init__(self):
        self.year = 0
        self.season = 0
        self.per_share_earnings = 0
        self.profit = 0
        self.profit_adding = 0
        self.profit2 = 0        #扣非净利润
        self.profit2_adding = 0
        self.sales = 0
        self.sales_adding = 0
        self.per_share_asset = 0  #每股净资产
        self.asset_adding = 0   #净资产收益率
        self.asset_adding2 = 0   #净资产收益率-摊薄

#financial data are stored in self._data{}
# _data[0] _data[1] _data[2] _data[3] --- 2009 first, second, third, forth season report data
# _data[4] _data[5] _data[6] _data[7] --- 2010 first, second, third, forth season report data

class FinancialHistory(BaseParser):
    MAX_YEARS = 10  #max years of data to save for parsing

    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)

        self._now = datetime.datetime.now()
        self._start = self._now.year - self.MAX_YEARS + 1

        self._data = {}
        for i in range(self.MAX_YEARS * 4):
            self._data[i] = None
        pass

    def doparse(self):
        datalist = list()
        with open(self._filepath) as f:
            for line in f:
                items = line.split()
                if len(items) < 8:
                    continue
                datalist.append(items)

        i = 0
        for date in datalist[0]:
            year, season = self.year_season(date)
            index = self.getindex(year, season)
            if index == -1:
                i += 1
                continue
            fd = FcData()
            fd.year = year
            fd.season = season
            fd.per_share_earnings = float(datalist[1][i].strip())
            fd.profit = self.parsemoney(datalist[2][i])
            fd.profit_adding = self.parseadding(datalist[3][i])
            fd.profit2 = self.parsemoney(datalist[4][i])        #扣非净利润
            fd.profit2_adding = self.parseadding(datalist[5][i])
            fd.sales = self.parsemoney(datalist[6][i])
            fd.sales_adding = self.parseadding(datalist[7][i])
            fd.per_share_asset = self.parsemoney(datalist[8][i])  #每股净资产
            fd.asset_adding = self.parseadding(datalist[9][i])   #净资产收益率
            fd.asset_adding2 = self.parseadding(datalist[10][i])   #净资产收益率

            self._data[index] = fd
            i += 1
        if not self.verify():
            raise ValueError(self._filepath + " parsing verifying failed")

    def parseadding(self, text):
        ret = text.replace("%", "")
        try:
            return float(ret)
        except:
            return None

    def parsemoney(self, text):
        ret = 0
        try:
            if "亿" in text:
                ret = float(text.replace("亿", "").strip()) * 10000 * 10000
            elif "万" in text:
                ret = float(text.replace("万", "").strip()) * 10000
            else:
                ret = float(text.strip())
            return ret
        except:
            return None

    def year_season(self, date):
        items = date.split("-")
        year = int(items[0])
        month = int(items[1])
        if month > 0 and month < 4:
            season = 0
        elif month > 3 and month < 7:
            season = 1
        elif month > 6 and month < 10:
            season = 2
        elif month > 9 and month < 13:
            season = 3
        else:
            season = -1
        return (year, season)

    def verify(self):
        for index in self._data:
            fd = self._data[index]
            if fd == None:
                continue
            if fd.per_share_asset == None or fd.per_share_earnings == None:
                continue
            val = fd.per_share_earnings * 100 / fd.per_share_asset
            tmp = abs(val - fd.asset_adding2)
            if tmp > 1:
                print "Warning: in ", fd.year, fd.season, fd.asset_adding2, val, ": diff is " + str(tmp)
        return True

    def getindex(self, year, season):
        if year > self._now.year:
            return -1
        if year <= (self._now.year - self.MAX_YEARS):
            return -1
        if season < 0:
            return -1
        if season > 3:
            return -1
        index = (year - self._start)*4 + season
        return index

    def get_year_report(self, year):
        index = self.getindex(year, 3)
        return self._data[index]

    def test(self):
        for y in range(2009, 2018 + 1):
#            for s in range(0, 4):
#                print y, s, str(self.getindex(y, s))
#            data = self.get_year_report(y)
#            if data != None:
#                print y, data.per_share_earnings
            pass


if __name__ == "__main__":
    fh = FinancialHistory("tmp/ylgf-finance")
    fh.doparse()
    fh.test()
    pass

