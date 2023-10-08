# InteractiveBrokers Backtesting

This repository provides a simple Python3 template for creating and running backtesting algorithms on a historical dataset of a specific security.

## Getting started
In the code example I obtain data for Tesla Inc. and generate buy/sell signals based on a simple heuristic.

1. Download and run the IB Client Portal API: `./bin/run.sh root/conf.yaml`
2. Authenticate through the local portal: `https://localhost:5000`
3. Once authenticated you can make HTTP requests to obtain historical data: `https://localhost:5000/v1/api/iserver/marketdata/history?conid=76792991&period=14d&bar=1h&outsideRth=true` (the `conid` is for TSLA)

## Code
1. Ensure the Client Portal up and authenticated.
2. Run `python3 backtest.py`
3. ...