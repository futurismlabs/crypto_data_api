import datetime
from binance.client import Client

client = Client()
params = {
	'symbol': 'BTCUSDT',
	'interval': '1h',
	'startTime': None,
	'endTime': int(datetime.datetime.now().timestamp() * 1000)
}
data = client._get('klines', data=params, version='v3')
print(data)