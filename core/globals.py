from utils.stockidname import StockIdName
from fileparsers.holdedstocks import HoldedStocks

from os import listdir
from os.path import isfile, join

from config import Config

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
        try:
            price = float(self.holded.holded[str(idx)][4])
        except:
            price = 0

        return price

    def getstocktotal(self, idx):
        try:
            total = float(self.holded.holded[str(idx)][6])
        except:
            total = 0

        return total




if __name__ == "__main__":
    glb = Globals.get_instance()
    print glb.sin.getname(300230)
    print glb.getstockprice(300230)
    pass
