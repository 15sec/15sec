from datetime import datetime
import backtrader


class Rsi(backtrader.Strategy):
    params = dict(period=20, devfactor=2)

    def __init__(self):
        self.order = None
        self.rsi = backtrader.ind.RSI_SMA(self.data.close, period=21)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy()
        else:
            if self.rsi > 70:
                self.sell()

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                log_text = '매수 {0:,.0f}원 ({1:,.0f}주)'.format(order.executed.price, order.executed.size)
                self.log(log_text)
            else:
                log_text = '매도 {0:,.0f}원 (자산: {1:,.0f}원)'.format(order.executed.price, cerebro.broker.getvalue())
                self.log(log_text)
            self.order = None
        else:
            self.order = None
            return

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print('[{0}] {1}'.format(dt.isoformat(), txt))


if __name__ == '__main__':
    cerebro = backtrader.Cerebro()

    # 2018년 5월 4일(액면 분할 이후)부터 2021년 9월까지 삼성전자 데이터
    data = backtrader.feeds.YahooFinanceData(dataname='005930.KS',
                                             fromdate=datetime(2018, 5, 4), todate=datetime(2021, 12, 1))

    cerebro.adddata(data)
    cerebro.addstrategy(Rsi)
    cerebro.broker.setcash(10000000)  # 초기자금 1000만원
    cerebro.broker.setcommission(commission=0.0014)  # 매수/매도시 나가므로 수수료 0.28의 절반
    cerebro.addsizer(backtrader.sizers.PercentSizer, percents=49)  # 비중 49%
    print('초기자산: {0:,.0f}원 (매수 비중: {1:,.0f}%)'.format(cerebro.broker.getvalue(), 49))
    cerebro.run()
    percent = ((cerebro.broker.getvalue() / 10000000) - 1.0) * 100
    print('최종자산: {0:,.0f}원(수익률: {1:,.2f}%)'.format(cerebro.broker.getvalue(), percent))
    #cerebro.plot(style='candlestick')
