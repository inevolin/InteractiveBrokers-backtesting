
import sys,json
sys.dont_write_bytecode = True
from urllib.request import urlopen
import ssl
from datetime import datetime
import random
import pandas as pd
import backtesting_core as core
import numpy as np

def run():
    # Getting historical data for TSLA (14day period, 1h sticks):
    jsonurl = urlopen('https://localhost:5000/v1/api/iserver/marketdata/history?conid=76792991&period=14d&bar=1h&outsideRth=true', context=ssl._create_unverified_context())
    
    # Market data HTTP response goes here
    resp = json.loads(jsonurl.read())
    
    market = resp['data']
    dt_breaks = []
    def work():
        portfolio = {}
        traceA = core.createNewScatterTrace("traceA", "y") # helper trace (optional)

        # date range initialization
        dt_all = pd.date_range(start=datetime.fromtimestamp(market[0]['t']/1000),end=datetime.fromtimestamp(market[-1]['t']/1000), freq='1H')
        dt_obs = [datetime.fromtimestamp(d['t']/1000).strftime('%Y-%m-%dT%H:%M') for d in market] # retrieve the dates that ARE in the original datset
        dt_breaks = [d for d in dt_all.strftime('%Y-%m-%dT%H:%M').tolist() if not d in dt_obs] # define dates with missing values
        
        prevs = []
        # iterating over each bar in the market range
        idx = 0
        for entry in market:
            dt = datetime.fromtimestamp(entry['t']/1000)
            c = entry['c']
            o = entry['o']
            l = entry['l']
            h = entry['h']
            price = random.uniform(l, h)  # simulating current price

            core.portfolioPriceEntry(portfolio, dt, price, o, c, l, h)

            # Custom algorithm:
            # generating buy/sell signals
            if len(prevs) == 2:
                z = np.polyfit(np.arange(0,len(prevs)+1), [p['c'] for p in prevs]+[price], 1) # linear regression
                # core.addToScatterTrace(traceA, dt, o+z[0])
                if (z[0] > 0.7 and dt.hour < 14):
                    core.portfolioBuy(portfolio, dt, price, 0) # buy signal
                if (z[0] < 0.3 and dt.hour > 16):
                    core.portfolioSell(portfolio, dt, price, 0) # sell signal
                prevs = prevs[1:] # pop first
            idx+=1
            prevs.append(entry)

        proc = core.processPortfolio(portfolio, 1)
        return (proc, portfolio, [traceA], dt_breaks)

    (proc, portfolio, traces, dt_breaks) = work()
    print("ROI: %f" % (proc['_']['ROI%']))
    core.portfolioToChart_OHLC(portfolio, traces, dt_breaks)

if __name__ == '__main__':
    run()
