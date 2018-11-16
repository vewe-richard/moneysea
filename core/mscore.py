from stock.parser import Parser
from globals import Globals

class Core:
    def __init__(self):
        pass

    def holded(self):
        holded = Globals.get_instance().holded.holded

        
        for idx in holded:
            stockdir = Globals.get_instance().stockpath(holded[idx][0])
            if stockdir == None:
                continue
            psr = Parser(stockdir)
            psr.outputSimple()
        pass

    def selected(self):
        pass

    def verbose(self, stockdir):
        psr = Parser(stockdir)
        psr.outputVerbose()
        pass
