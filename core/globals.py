from utils.stockidname import StockIdName
from fileparsers.holdedstocks import HoldedStocks

from os import listdir
from os.path import isfile, join

from config import Config
from fileparsers.ranklist import RankList

class Globals:
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self.sin = StockIdName()

        #find latest current file
        current = self.currentholdedstocks()
        self.holded = HoldedStocks(current)
        self.holded.doparse()

        self.stockspath = {}
        self.initstockspath()

        try:
            self.rl = RankList(Config.SELECTED_PATH)
            self.rl.doparse()
        except:
            self.rl = None

        self.option = Config.OPTION_HOLDED

    def selectedItems(self):
        if self.rl != None:
            return self.rl.items
        else:
            return None

    def setOption(self, option):
        self.option = option

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Globals()
        return cls.INSTANCE

    def currentholdedstocks(self):
        tmp = "current-"
        for f in listdir(Config.CURRENT_HOLDED_PATH):
            if "current-" in f:
                if f > tmp:
                    tmp = f
        return Config.CURRENT_HOLDED_PATH + "/" + tmp

    def getstockprice(self, idx):
        #try find in current
        s = "%06d"%(idx)
        if self.option == Config.OPTION_SELECTED:
            try:
                price = float(self.rl.items[s])
                return price
            except:
                return 0

        try:
            price = float(self.holded.holded[s][4])
        except:
            price = 0

        return price

    def getstocktotal(self, idx):
        s = "%06d"%(idx)
        try:
            total = float(self.holded.holded[s][6])
        except:
            total = 0

        return total

    def stockpath(self, idx):
        try:
            return self.stockspath[idx]
        except:
            return None

    def initstockspath(self):
        for f in listdir(Config.STOCKS_PATH):
            items = f.split("-")
            if len(items) >= 2:
                self.stockspath[items[1]] = Config.STOCKS_PATH + "/" + f




if __name__ == "__main__":
    glb = Globals.get_instance()
    print glb.sin.getname(300230)
    print glb.getstockprice(300230)
    pass
