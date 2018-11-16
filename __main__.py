# coding=gbk
import sys
import getopt
from mscore import Core


class MoneySea:
    def __init__(self):
        pass

    def usage(self):
        print "python __main__.py [-h | -s filepath | -v stockdir]"
        print "         -h: show holded stocks in simple format"
        print "         -s: show selected stocks in filepath"
        print "         -v: show verbose info of this stock"
        print ""

    def run(self):
        self._core = Core()
        self.input()
        pass

    def input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hsv", [])
        except:
            self.usage()
            sys.exit(2)

        for o, a in opts:
            if o == "-h":
                self._core.holded()
            elif o == "-s":
                self._core.selected(args[0])
            elif o == "-v":
                self._core.verbose(args[0])
        pass


if __name__ == "__main__":
    ms = MoneySea()
    ms.run()






