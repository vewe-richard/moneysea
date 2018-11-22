# coding=utf-8
# 对每一只股票
# 显示股票名字
# 自变量：年份 - 初始年
# 变量：（年净利率 - 初始年净利率）/ 初始年净利率
# 1. 显示上述关系的散列图
# 2. 对上述关系进行线性拟合，所得的直线图

import sys

from fileparsers.financial import FinancialHistory

from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np


class PredictAdding:
    def __init__(self, filepath):
        self._filepath = filepath
        pass

    def run(self):
        fh = FinancialHistory(self._filepath + "finance")
        fh.doparse()

        start = 30000
        start_profit = 0
        ax = []
        ay = []
        for y in range(fh._start, fh._now.year + 1):
            data = fh.get_year_report(y)
            if data == None:
                continue
            if y < start:
                start = y
                start_profit = data.profit

            print y, y - 2009, data.profit, (data.profit - start_profit)/start_profit
            ax.append(y-2009)
            ay.append((data.profit - start_profit)/start_profit)

#        print ax
#        print ay
        # if start_profit < 0 # not acceptable
        nx = np.array(ax)
        ny = np.array(ay)

        regr = linear_model.LinearRegression()
        regr.fit(nx.reshape(-1, 1), ny)
        a, b = regr.coef_, regr.intercept_
        print "adding:", a[0], b
        print "score:", regr.score(nx.reshape(-1, 1), ny)


        plt.scatter(nx, ny, color='blue')
        plt.plot(nx, regr.predict(nx.reshape(-1,1)), color='red', linewidth=4)
        plt.show()
        pass

    def test(self):
        regr = linear_model.LinearRegression()

        x = np.array([0,1,2,3,4])
        y = np.array([1,3,5,7,9])
        print x
        print y
        print x.reshape(-1, 1)
        regr.fit(x.reshape(-1, 1), y)
        

        a, b = regr.coef_, regr.intercept_
        print a, b
        print type(a)
        print type(b)
        print a[0]
        print type(a[0])
        pass


if __name__ == "__main__":
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    print sys.argv[1]

    pa = PredictAdding(sys.argv[1])
    pa.run()
#    pa.test()
