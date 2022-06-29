# Futurism Labs Crypto Data API

A public crypto data API for toy projects.

This module can be installed from: https://pypi.org/project/cryptodataapi/

Open your python terminal and type:

```bash
pip install cryptodataapi
```

For examples on how to use this library please check the code in each of:

- cryptodataapi/binance_api.py
- cryptodataapi/bybit_api.py

For Binance:

```python
from cryptodataapi.binance_api import BinanceAPI

if __name__ == '__main__':
    api = BinanceAPI()

    info = api.get_spot_info()
    print(info)

    # 1. Spot Symbols
    symbols = api.get_spot_symbols()
    print(symbols)

    # 2. Low level request of spot OHLCV data
    btcusdt = api._get_spot_data(symbol='BTCUSDT', interval='1h')
    print(btcusdt)

    # 3. Spot OHLCV API request
    btcusdt = api.get_spot_data(symbol='BTCUSDT', interval='1m', count=100)
    print(btcusdt)

    # 4. Request OHLCV data by month
    data = api.get_spot_data_by_month(symbol='BTCUSDT', year=2021, month=1)
    print(data)
```

And for Bybit:

```python
from cryptodataapi.bybit_api import BybitAPI

if __name__ == '__main__':
    api = BybitAPI()

    spot = api.get_spot_symbols()
    print(spot)

    btcusdt = api.get_spot_data(symbol='BTCUSDT', interval='60m', count=1000)
    print(btcusdt)
```

Current status of this project is: Work in Progress

And though it only supports calling Spot data for of now, it will extend its usage in time to come.