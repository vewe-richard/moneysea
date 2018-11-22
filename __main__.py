# coding=gbk
import sys
import getopt
from mscore import Core
import os
from config import Config
from shutil import copyfile
from globals import Globals

class MoneySea:
    def __init__(self):
        pass

    def usage(self):
        print "python __main__.py [-h | -s | -S filepath | -v stockdir [-p] | -u | -t]"
        print "         -h: show holded stocks in simple format"
        print "         -s: show selected stocks"
        print "         -v: show verbose info of this stock"
        print "         -S: set selected stocks file"
        print "         -p: only for -v function, indicate using info in selected stocks"
        print "         -u: update price list"
        print "         -t: run test"
        print ""

    def run(self):
        self._core = Core()
        self.input()
        pass

    def input(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hsv:S:put", [])
        except:
            self.usage()
            sys.exit(2)

        for o, a in opts:
            if o == "-p":
                Globals.get_instance().setOption(Config.OPTION_SELECTED)

        for o, a in opts:
            if o == "-h":
                self._core.holded()
            elif o == "-s":
                self._core.selected()
            elif o == "-v":
                self._core.verbose(a)
            elif o == "-S":
                try:
                    os.unlink(Config.SELECTED_PATH)
                except:
                    pass
                copyfile(a, Config.SELECTED_PATH)
            elif o == "-u":
                self._core.updateprice()
            elif o == "-t":
                self._core.test()
        pass


if __name__ == "__main__":
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    ms = MoneySea()
    ms.run()






