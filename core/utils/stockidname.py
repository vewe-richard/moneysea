
from config import Config
from fileparsers.stockidnamemapfile import StockIdNameMapFile

class StockIdName:
    def __init__(self):
        self._sha = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_SHA)
        self._sha.doparse()
        self._sz = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_SZ)
        self._sz.doparse()
        self._open = StockIdNameMapFile(Config.STOCK_ID_NAME_MAP_OPEN)
        self._open.doparse()
        pass

    def getname(self, sid):
        name = None
        try:
            name = self._sha._map[sid]
        except:
            try:
                name = self._sz._map[sid]
            except:
                try:
                    name = self._open._map[sid]
                except:
                    name = "Unknown"
        return name


if __name__ == "__main__":
    sin = StockIdName()
    print sin.getname(600004)
    print sin.getname(000002)
    print sin.getname(300230)
    pass
