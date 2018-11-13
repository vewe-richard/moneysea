# coding=utf-8
# file source: On Ubuntu, using chromium to open 招商证券, login in and select 资金股份, copy and paste to vim
# Provide: 总资产，市值，余额；每只股票和它对应的信息
# Verify: 总资产应该等于市值加余额; 其中每只股票的市值和等于总市值
# Provide: holded date


from baseparser import BaseParser

class HoldedStocks(BaseParser):
    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)
        pass

    def doparse(self):
        self.holded = {}
        with open(self._filepath) as f:
            prev_not_null_line = None
            for line in f:
                if "总资产（元）" in line:
                    self.total =  float(prev_not_null_line.strip().replace(",", ""))
                elif "市值（元）" in line:
                    self.market = float(prev_not_null_line.strip().replace(",", ""))
                elif "余额（元）" in line:
                    self.cash = float(prev_not_null_line.strip().replace(",", ""))
                elif "人民币" in line:
                    self.addstock(line)

                if len(line.strip()) > 1:
                    prev_not_null_line = line

        if not self.verify():
            raise ValueError("file parser verifying failed")

    def verify(self):
        if abs(self.total - self.market - self.cash) > 200:
            return False
        total = 0
        for stock in self.holded:
            total += float(self.holded[stock][6].strip())
        if abs(self.market - total) > 200:
            return False
        return True

    def addstock(self, line):
        items = line.strip().split()
        if len(items) < 12:
            return
        self.holded[items[0]] = items

    def date(self):
        index = self._filepath.find("current-")
        if index == -1:
            raise ValueError("incorrect file name format")
        return self._filepath[(index + len("current-")):]


if __name__ == "__main__":
    hs = HoldedStocks("tmp/current-20181110a")
    hs.doparse()
    print hs.date()
    pass
