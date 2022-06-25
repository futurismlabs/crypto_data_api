import time
import datetime
import pandas as pd
from binance.client import Client


class BinanceAPI:

    def __init__(self):
        self.client = Client()

    def get_tickers(self):
        return self.client.get_all_tickers()

    def get_spot_info(self):
        return self.client.get_exchange_info()

    def get_spot_tickers(self):
        info = self.get_spot_info()
        is_spot = lambda d: 'USDT' in d['symbol'] and 'SPOT' in d['permissions']
        symbols = [d['symbol'] for d in info['symbols'] if is_spot(d)]
        return symbols

    def _get_spot_data(self,
                       symbol: str,
                       interval: str,
                       start_time: int = None,
                       end_time: int = int(datetime.datetime.now().timestamp() * 1000)):
        """
        :param symbol: BTCUSDT
        :param interval: 1m, 3m, 5m, 10m, 15m, 1h, 4h, 1d
        :param start_time: timestamp
        :param end_time: timestamp
        :return: pd.DataFrame
        """
        columns = [
            'Open time',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Close time',
            'Quote asset volume',
            'Number of trades',
            'Taker buy base asset volume',
            'Taker buy quote asset volume',
            'Ignore'
        ]
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1000
        }
        data = self.client._get('klines', data=params, version='v3')
        df = pd.DataFrame(data)
        df.columns = columns
        df['Open time'] = df['Open time'].apply(lambda t: datetime.datetime.fromtimestamp(t // 1000))
        df['Close time'] = df['Close time'].apply(lambda t: datetime.datetime.fromtimestamp(t // 1000))
        return df

    def get_spot_data(self,
                      symbol: str,
                      interval: str,
                      count: int):
        mins = int(interval.replace('m', ''))
        if mins >= 60:
            interval = f'{mins // 60}h'
        data = self._get_spot_data(symbol, interval)
        if len(data) >= count:
            return data.iloc[-count:].reset_index(drop=True)
        else:
            result = data
            result_len = len(result)
            while len(result) < count:
                time.sleep(0.1)
                end_time = int(result.iloc[0]['Open time'].timestamp() * 1000)
                data = self._get_spot_data(symbol, interval, end_time=end_time)
                data = data[~data['Open time'].isin(result['Open time'])]
                result = pd.concat([data, result], axis=0)
                if result_len != len(result):
                    result_len = len(result)
                else:
                    break
            return result[-count:].reset_index(drop=True)


if __name__ == '__main__':
    api = BinanceAPI()

    # 1. Spot Tickers
    tickers = api.get_spot_tickers()
    print(tickers)

    # 2. Low level request of spot OHLCV data
    btcusdt = api._get_spot_data(symbol='BTCUSDT', interval='1h')
    print(btcusdt)

    # 3. Spot OHLCV API request
    btcusdt = api.get_spot_data(symbol='BTCUSDT', interval='1m', count=100000)
    print(btcusdt)
