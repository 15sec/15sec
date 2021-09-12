from datetime import datetime
import backtrader


class CrossStrategy(backtrader.Strategy):

    params = dict(period1=5, period2=20)

    def __init__(self):
        sma1 = backtrader.ind.SMA(period=self.p.period1) # 5일 이동 평균선
        sma2 = backtrader.ind.SMA(period=self.p.period2) # 20일 이동 평균선
        self.crossover = backtrader.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()


if __name__ == '__main__':
    cerebro = backtrader.Cerebro()
    # 2011년 9월부터 2021년 9월까지 삼성전자 데이터
    data = backtrader.feeds.YahooFinanceData(dataname='005930.KS',
                                             fromdate=datetime(2011, 9, 1), todate=datetime(2021, 9, 1))
    cerebro.adddata(data)
    cerebro.addstrategy(CrossStrategy)
    cerebro.broker.setcash(10000000)  # 초기자금 1000만원
    cerebro.broker.setcommission(commission=0.0014)  # 매수/매도시 나가므로 수수료 0.28의 절반
    cerebro.addsizer(backtrader.sizers.PercentSizer, percents=49)
    print('초기자금: {0:,.0f}원'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('최종자금: {0:,.0f}원'.format(cerebro.broker.getvalue()))
    percent = ((cerebro.broker.getvalue() / 10000000) - 1.0) * 100
    print('수익률: {0:,.0f}%'.format(percent))
    cerebro.plot(style='candlestick')
