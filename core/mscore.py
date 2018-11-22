# coding=utf-8
from stock.parser import Parser
from globals import Globals
from config import Config
from utils.pricelist import PriceList
from test.earningadding import EarningAdding
from growinglist import GrowingList
from stock.adjust import Adjust


class Core:
    def __init__(self):
        pass

    def holded(self):
        Globals.get_instance().setOption(Config.OPTION_HOLDED)
        holded = Globals.get_instance().holded.holded
        
        liststocks = {}
        for idx in holded:
            stockdir = Globals.get_instance().stockpath(holded[idx][0])
            if stockdir == None:
                liststocks[idx] = None
                continue
            psr = Parser(stockdir)
#            psr.outputSimple()
            liststocks[idx] = psr.getSummer()

        print Parser.getTitle()
        for summer in liststocks:
            if liststocks[summer] == None:
                print "%9s,%8s"%(Globals.get_instance().sin.getname(int(summer)), summer)
                continue
            if Globals.get_instance().getstocktotal(int(summer)) < 10.0:
                continue
            s = liststocks[summer]
            print Parser.summerFormat() % Parser.formatdata(s)
        pass

    def growinglist(self):
        gl = GrowingList()
        gl.run()
        gl.output()
        pass

    def adjust(self, params):
        print params
        n = 0
        p = 0
        for item in params:
            vals = item.split("=")
            if vals[0] == "n":
                print "n:", vals[1]
                n = int(vals[1])
            elif vals[0] == "p":
                print "p:", vals[1]
                p = float(vals[1])
            else:
                print "Error: see help"
                return

        if n == 0 or p == 0:
            print "Please set n and p value"
            return
        print n, p
        ad = Adjust(n, p)
        ad.run()
        ad.output()

    def selected(self):
        Globals.get_instance().setOption(Config.OPTION_SELECTED)
        items = Globals.get_instance().selectedItems()
        if items == None:
            print "No selected file is set"
            return

        liststocks = {}
        for idx in items:
            stockdir = Globals.get_instance().stockpath(idx)
            if stockdir == None:
                liststocks[idx] = None
                continue
            psr = Parser(stockdir)
            liststocks[idx] = psr.getSummer()

        print Parser.getTitle()
        for summer in liststocks:
            if liststocks[summer] == None:
                print "%9s,%8s"%(Globals.get_instance().sin.getname(int(summer)), summer)
                continue
            s = liststocks[summer]
            print Parser.summerFormat() % Parser.formatdata(s)
        pass

    def verbose(self, stockdir):
        psr = Parser(stockdir)
        psr.outputVerbose()
        pass

    def updateprice(self):
        pl = PriceList()
        pl.run()
        pass

    def test(self):
        ea = EarningAdding()
        ea.run()
        pass
