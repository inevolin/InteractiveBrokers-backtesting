# InteractiveBrokers Backtesting

This repository provides a simple Python3 template for creating, running and visualizing backtesting algorithms on a traded security.

## Getting started
1. Download and run the IB Client Portal API: `./bin/run.sh root/conf.yaml`
2. Authenticate through the local portal: `https://localhost:5000`
3. Once authenticated you can make HTTP requests to obtain historical data: `https://localhost:5000/v1/api/iserver/marketdata/history?conid=76792991&period=14d&bar=1h&outsideRth=true` (the `conid` is for TSLA)

## Code
In the code example I obtain data for Tesla Inc. and generate buy/sell signals based on a simple heuristic.

1. Ensure the Client Portal up and authenticated.
2. Run `python3 backtest.py`.
3. A new browser tab will open with the candlestick chart and buy/sell indicates according to the heuristic/algorithm.
4. The script will output the ROI of the buy/sell signals (excluding transaction fees) `ROI: -5.140722` (in %).

![tsla](https://github.com/inevolin/InteractiveBrokers-backtesting/assets/53948000/ab29e8d1-ed60-4fcf-b336-7ed28e402880)
