import sys
sys.dont_write_bytecode = True

import math
import requests
import datetime
import random
import pprint
import sys
import json
import time
import copy
import collections
import urllib.request
from itertools import chain
import copy


def processPortfolio(portfolio, buy_ratio, sell_ratio=1, fee=0.001):

    # Reverse the portfolio order and remove all buys from the end,
    # this ensures our last trade is always a "sell", and if sell_ratio==1 then we can compute a valid ROI.
    # When sell_ratio is smaller than 1, then we won't have a clean exit and incomplete ROI.
    portfolio = collections.OrderedDict(reversed(sorted(portfolio.items())))
    for key, obj in portfolio.items():
        if '_buy' in obj:
            del obj['_buy']
        if '_sell' in obj:
            break
    portfolio = collections.OrderedDict(sorted(portfolio.items()))

    # iterate over dict and calculate profit/loss
    cash_start = 10000
    cash = cash_start
    crypto = 0
    lastBuyPrice = None    

    buytrades = 0
    selltrades = 0
    for key, obj in portfolio.items():
        if '_buy' in obj:
            if cash > 0:
                buyprice = obj['_buy']['buyprice']
                lastBuyPrice = buyprice
                crypto_x = cash*buy_ratio / buyprice
                crypto += crypto_x*(1-fee)
                obj['fee'] = crypto_x*fee
                cash -= cash*buy_ratio
                buytrades += 1
                if '_sell' in obj: del obj['_sell']
            else:
                del obj['_buy']
        
        if '_sell' in obj:
            if crypto > 0: 
                sellprice = obj['_sell']['sellprice']
                cash_x = crypto*sell_ratio * sellprice
                cash += cash_x*(1-fee)
                obj['fee'] = cash*fee
                crypto -= crypto*sell_ratio
                selltrades += 1
                if '_buy' in obj: del obj['_buy']
            else:
                del obj['_sell']

        obj['crypto'] = crypto
        obj['cash'] = cash
        portfolio[key] = collections.OrderedDict(sorted(portfolio[key].items()))

    portfolio['_'] = {
        'cash':cash,
        'margin': cash - cash_start,
        'ROI%': ((cash / cash_start)-1)*100,
        'crypto':crypto,
        'buytrades': buytrades,
        'selltrades': selltrades,
    }
    portfolio = collections.OrderedDict(sorted(portfolio.items()))

    return portfolio

def portfolioPriceEntry(portfolio, dtit, price, open, close, low, high):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    if dtit_s not in portfolio: portfolio[dtit_s] = {}

    portfolio[dtit_s]["ap"]= price # ap = actual price
    portfolio[dtit_s]["open"]= open
    portfolio[dtit_s]["close"]= close
    portfolio[dtit_s]["low"]= low
    portfolio[dtit_s]["high"]= high

def portfolioBuy(portfolio, dtit, buyprice, uncertainty_margin):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    if dtit_s not in portfolio: portfolio[dtit_s] = {}

    portfolio[dtit_s]['_buy']=(
        {
            'buyprice_default':buyprice,
            'buyprice':buyprice*(1+uncertainty_margin)
        }
    )
def portfolioSell(portfolio, dtit, sellprice, uncertainty_margin):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    if dtit_s not in portfolio: portfolio[dtit_s] = {}

    portfolio[dtit_s]['_sell']=(
        {
            'sellprice_default':sellprice,
            'sellprice':sellprice*(1-uncertainty_margin)
        }
    )
def createNewScatterTrace(name, yaxis, mode='lines'):
    return {
    'x':[],
    'y':[],
    'z':[],
    'name': name,
    'mode': mode,
    'yaxis':yaxis}

def addToScatterTrace(trace, dtit, value):
    dtit_s = datetime.datetime.strftime(dtit, '%Y-%m-%d %H:%M')
    trace['x'].append(dtit_s)
    trace['y'].append(value)

def getHistory():
    return [{"o":245,"c":249.72,"h":252.99,"l":244.86,"v":202164,"t":1693920600000},{"o":249.73,"c":253.09,"h":253.88,"l":249.03,"v":235777,"t":1693922400000},{"o":253.1,"c":252.74,"h":253.99,"l":252.09,"v":125959,"t":1693926000000},{"o":252.76,"c":256.48,"h":256.9,"l":252.61,"v":141329,"t":1693929600000},{"o":256.46,"c":255.88,"h":256.66,"l":255.1,"v":110578,"t":1693933200000},{"o":255.92,"c":257.89,"h":258,"l":255.54,"v":110263,"t":1693936800000},{"o":257.89,"c":256.49,"h":257.93,"l":255.95,"v":121889,"t":1693940400000},{"o":255.14,"c":249.71,"h":255.39,"l":248.11,"v":177539,"t":1694007000000},{"o":249.63,"c":246.12,"h":253.11,"l":245.06,"v":235545,"t":1694008800000},{"o":246.11,"c":248.63,"h":248.89,"l":245.53,"v":121169,"t":1694012400000},{"o":248.63,"c":248.49,"h":249.71,"l":247.41,"v":102021,"t":1694016000000},{"o":248.49,"c":250.93,"h":251.99,"l":248.32,"v":129995,"t":1694019600000},{"o":250.96,"c":251.75,"h":252.44,"l":250.15,"v":97983,"t":1694023200000},{"o":251.74,"c":251.99,"h":252.3,"l":250.96,"v":105357,"t":1694026800000},{"o":245.07,"c":246.19,"h":248.7,"l":243.26,"v":161786,"t":1694093400000},{"o":246.18,"c":245.31,"h":247.36,"l":243.51,"v":204991,"t":1694095200000},{"o":245.34,"c":247.2,"h":247.57,"l":245.31,"v":117515,"t":1694098800000},{"o":247.19,"c":250.01,"h":250.74,"l":246.83,"v":119974,"t":1694102400000},{"o":249.99,"c":252.09,"h":252.18,"l":249.58,"v":104455,"t":1694106000000},{"o":252.07,"c":251.84,"h":252.81,"l":250.21,"v":109835,"t":1694109600000},{"o":251.83,"c":251.49,"h":252.34,"l":250.91,"v":107469,"t":1694113200000},{"o":251.22,"c":253.74,"h":256.52,"l":250.31,"v":178696,"t":1694179800000},{"o":253.76,"c":251.65,"h":255.48,"l":251.65,"v":186974,"t":1694181600000},{"o":251.63,"c":253.09,"h":254.35,"l":251.4,"v":123595,"t":1694185200000},{"o":253.09,"c":249.98,"h":253.14,"l":249.07,"v":144702,"t":1694188800000},{"o":249.98,"c":248.03,"h":249.98,"l":246.67,"v":140025,"t":1694192400000},{"o":248.02,"c":247.58,"h":248.88,"l":246.84,"v":110328,"t":1694196000000},{"o":247.55,"c":248.46,"h":248.78,"l":246.94,"v":106156,"t":1694199600000},{"o":264.13,"c":264.35,"h":265.94,"l":260.61,"v":246055,"t":1694439000000},{"o":264.35,"c":265.96,"h":266.34,"l":262.61,"v":238840,"t":1694440800000},{"o":265.96,"c":271.55,"h":272.53,"l":265.92,"v":253210,"t":1694444400000},{"o":271.57,"c":270.78,"h":272.5,"l":270.35,"v":151217,"t":1694448000000},{"o":270.78,"c":273,"h":273.06,"l":270.63,"v":135104,"t":1694451600000},{"o":273,"c":274.37,"h":274.64,"l":272.28,"v":136601,"t":1694455200000},{"o":274.39,"c":273.65,"h":274.85,"l":272.55,"v":170163,"t":1694458800000},{"o":270.76,"c":277.48,"h":278.14,"l":268.33,"v":214888,"t":1694525400000},{"o":277.5,"c":271.94,"h":278.39,"l":271.59,"v":265830,"t":1694527200000},{"o":271.92,"c":271.22,"h":273.2,"l":269.91,"v":155058,"t":1694530800000},{"o":271.21,"c":269.25,"h":272.23,"l":268.92,"v":108912,"t":1694534400000},{"o":269.24,"c":267.41,"h":271.14,"l":267,"v":130838,"t":1694538000000},{"o":267.4,"c":267.43,"h":268.18,"l":266.6,"v":110933,"t":1694541600000},{"o":267.41,"c":267.39,"h":268.42,"l":266.89,"v":115929,"t":1694545200000},{"o":270.07,"c":272.61,"h":274.98,"l":268.61,"v":191003,"t":1694611800000},{"o":272.58,"c":272.26,"h":273.15,"l":268.1,"v":200428,"t":1694613600000},{"o":272.27,"c":271.23,"h":273.19,"l":270.25,"v":122679,"t":1694617200000},{"o":271.24,"c":271.87,"h":272.45,"l":270,"v":93808,"t":1694620800000},{"o":271.88,"c":272.8,"h":273.68,"l":271.12,"v":87490,"t":1694624400000},{"o":272.8,"c":271.16,"h":273.03,"l":270.56,"v":95845,"t":1694628000000},{"o":271.19,"c":271.28,"h":271.5,"l":270,"v":102702,"t":1694631600000},{"o":271.23,"c":273.95,"h":274.51,"l":270.42,"v":163796,"t":1694698200000},{"o":273.96,"c":274.63,"h":275.71,"l":271.57,"v":211618,"t":1694700000000},{"o":274.63,"c":274.92,"h":276.18,"l":273.35,"v":129525,"t":1694703600000},{"o":274.92,"c":275.15,"h":275.5,"l":274.03,"v":85878,"t":1694707200000},{"o":275.15,"c":274.97,"h":275.87,"l":274.4,"v":78901,"t":1694710800000},{"o":274.97,"c":276.41,"h":276.54,"l":274.84,"v":96577,"t":1694714400000},{"o":276.42,"c":276.02,"h":276.71,"l":275.27,"v":90876,"t":1694718000000},{"o":277.54,"c":272.25,"h":278.98,"l":271.65,"v":198705,"t":1694784600000},{"o":272.27,"c":273.25,"h":276.04,"l":271.98,"v":218816,"t":1694786400000},{"o":273.24,"c":275.18,"h":275.48,"l":273.19,"v":126908,"t":1694790000000},{"o":275.19,"c":276.3,"h":276.56,"l":274.2,"v":109078,"t":1694793600000},{"o":276.31,"c":274.37,"h":276.5,"l":274,"v":88838,"t":1694797200000},{"o":274.37,"c":273.2,"h":274.4,"l":271,"v":124642,"t":1694800800000},{"o":273.19,"c":274.42,"h":278,"l":272.34,"v":127844,"t":1694804400000},{"o":271,"c":266.15,"h":271.44,"l":263.76,"v":170762,"t":1695043800000},{"o":266.11,"c":266.52,"h":268.41,"l":264.48,"v":179090,"t":1695045600000},{"o":266.51,"c":267.2,"h":268.64,"l":265.92,"v":105904,"t":1695049200000},{"o":267.21,"c":267.29,"h":267.99,"l":266.25,"v":80402,"t":1695052800000},{"o":267.29,"c":267.17,"h":268.43,"l":266.7,"v":69864,"t":1695056400000},{"o":267.19,"c":265.29,"h":267.58,"l":264.76,"v":84634,"t":1695060000000},{"o":265.29,"c":265.2,"h":266.24,"l":264.71,"v":99996,"t":1695063600000},{"o":264.35,"c":261.94,"h":267.85,"l":261.53,"v":161797,"t":1695130200000},{"o":261.94,"c":263.03,"h":264.98,"l":261.2,"v":181642,"t":1695132000000},{"o":263.02,"c":264.93,"h":265.28,"l":262.93,"v":111910,"t":1695135600000},{"o":264.91,"c":265.18,"h":265.42,"l":263.56,"v":87762,"t":1695139200000},{"o":265.19,"c":267.13,"h":267.42,"l":265.03,"v":105569,"t":1695142800000},{"o":267.15,"c":265.66,"h":267.5,"l":265.56,"v":96775,"t":1695146400000},{"o":265.63,"c":266.49,"h":266.79,"l":265.22,"v":94514,"t":1695150000000},{"o":267.09,"c":267.08,"h":268.37,"l":265.31,"v":131542,"t":1695216600000},{"o":267.13,"c":266.83,"h":268.6,"l":266.47,"v":143070,"t":1695218400000},{"o":266.83,"c":267.08,"h":267.19,"l":265.46,"v":84923,"t":1695222000000},{"o":267.07,"c":268.28,"h":268.43,"l":266.77,"v":72171,"t":1695225600000},{"o":268.29,"c":271.27,"h":273.93,"l":268.01,"v":184791,"t":1695229200000},{"o":271.3,"c":270.39,"h":273.55,"l":269.2,"v":181743,"t":1695232800000},{"o":270.32,"c":262.48,"h":271,"l":262.46,"v":197956,"t":1695236400000},{"o":257.85,"c":255.71,"h":260.39,"l":254.21,"v":172743,"t":1695303000000},{"o":255.75,"c":257.31,"h":258.48,"l":255.08,"v":200974,"t":1695304800000},{"o":257.31,"c":257.78,"h":258.55,"l":256.63,"v":111976,"t":1695308400000},{"o":257.78,"c":259.14,"h":260.47,"l":257.01,"v":121140,"t":1695312000000},{"o":259.12,"c":258.58,"h":260.86,"l":258.53,"v":98569,"t":1695315600000},{"o":258.59,"c":256.92,"h":258.89,"l":256.39,"v":101343,"t":1695319200000},{"o":256.94,"c":255.7,"h":257.67,"l":255.22,"v":137633,"t":1695322800000},{"o":257.4,"c":256.56,"h":257.77,"l":256.2,"v":1484,"t":1695389400000}]

def portfolioToChart_OHLC(portfolio, traces=[], dt_breaks=[], file="./chart.html", shapes=[]):
    # this will use the portfolio and its _buy/_sell entries to generate an OHLC chart.
    import plotly
    import plotly.graph_objs as go

    opens = []
    highs = []
    lows = []
    closes = []
    dates = []

    annons = []
    
    for key, obj in portfolio.items():
        if key == "_": continue
        # dt = datetime.datetime.strptime(key, '%Y-%m-%d %H:%M') # if you use this, then plotly will display local dates -- but you must parse it everywhere below as well !
        dt = key
        opens.append(obj['open'])
        highs.append(obj['high'])
        lows.append(obj['low'])
        closes.append(obj['close'])
        dates.append( dt )
        if '_buy' in obj:
            annons.append(
                {
                    'x':dt,
                    'y':obj['_buy']['buyprice_default'],
                    'text':"B",
                    'arrowcolor': "black",
                }
            )

        if '_sell' in obj:
            annons.append(
                {
                    'x':dt,
                    'y':obj['_sell']['sellprice_default'],
                    'text':"S",
                    'arrowcolor': "blue",
                }
            )
        
    data = []
    trace = go.Candlestick(x=dates,
                        open=opens,
                        high=highs,
                        low=lows,
                        close=closes,
                        opacity=0.5)
    data.append(trace)

    for t in traces:
        trace = go.Scatter(
            name = t['name'],
            x = t['x'],
            y = t['y'],
            mode = t['mode'],#'lines', # +markers
            yaxis = t['yaxis'],
            connectgaps=True,
        )
        data.append(trace)

    layout = go.Layout(
        shapes = shapes,
        xaxis = dict(
            rangeslider = dict(
                visible = False
            ),
            type = "date",
        ),
        yaxis2= {
            'title': 'y2',
            'overlaying': 'y',
            'side': 'right',
            'showgrid':False,
            'autorange': True,
            'anchor': 'free',
            'position':0
        },
        yaxis3= {
            'title': 'y3',
            'overlaying': 'y',
            'side': 'right',
            'showgrid':False,
            'autorange': True,
            'anchor': 'free',
            'position': 0.3
        },
        yaxis4= {
            'title': 'y4',
            'overlaying': 'y',
            'side': 'right',
            'showgrid':False,
            'autorange': True,
            'anchor': 'free',
            'position': 0.6
        },
        annotations = annons,
       # dragmode = "pan"
    )
    
    fig = go.Figure(data=data,layout=layout)
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks, dvalue=60 * 60 * 1000)]) # this removes gaps (for 1hr interval bar charts)
    config = {'scrollZoom': True}
    plotly.offline.plot(fig, config=config, filename=file)
