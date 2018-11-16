from stock.parser import Parser
from globals import Globals

class Core:
    def __init__(self):
        pass

    def holded(self):
        holded = Globals.get_instance().holded.holded
        
        liststocks = {}
        for idx in holded:
            stockdir = Globals.get_instance().stockpath(holded[idx][0])
            if stockdir == None:
                continue
            psr = Parser(stockdir)
#            psr.outputSimple()
            liststocks[idx] = psr.getSummer()

        print Parser.getTitle()
        for summer in liststocks:
            s = liststocks[summer]
            print Parser.summerFormat() % Parser.formatdata(s)
        pass

    def selected(self):
        pass

    def verbose(self, stockdir):
        psr = Parser(stockdir)
        psr.outputVerbose()
        pass
