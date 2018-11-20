# coding=utf-8
from baseparser import BaseParser

class RankList(BaseParser):

    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)
        self.items = {}


    def doparse(self):
        with open(self._filepath) as f:
            for line in f:
                items = line.split()
                if len(items) < 11:
                    continue
                self.items[items[0]] = items[2]

        if not self.verify():
            raise ValueError(self._filepath + " parsing verifying failed")
        pass

    def verify(slef):
        return True


if __name__ == "__main__":
    rl = RankList("input/selected/20181119-ranklist")
    rl.doparse()
    print rl.items
