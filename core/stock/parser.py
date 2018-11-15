import os
from globals import Globals

class Parser:
    def __init__(self, stockpath):
        self._stockpath = stockpath
        self.doparse()
        pass

    def doparse(self):
        items = os.path.basename(os.path.dirname(self._stockpath)).split("-")
        self._id = int(items[0])
        self._name = Globals.get_instance().sin.getname(self._id)
        pass

    def getid(self):
        return self._id

    def getname(self):
        self._name


if __name__ == "__main__":
    psr = Parser("input/stocks/300230-ylgf/")

    print psr.getid()
    print psr.getname()
    pass
