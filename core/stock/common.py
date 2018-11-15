# coding=utf-8

class Common:
    def __init__(self):
        pass

    def pricesRange(self, pershareearnings):
        #recording prices per 收益 15% 10% 5%
        return (100*pershareearnings/15, 100*pershareearnings/10, 100*pershareearnings/5)
