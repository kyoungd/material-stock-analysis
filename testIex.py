
import pyEX as p


async def print_data(data):
    print(data)


# token1 = 'pk_4c4cea17cf834cafadd2a57e5bd7f2cc'
# c = p.Client(api_token=token1, version='v1', api_limit=5)
c = p.Client(version='sandbox')
c.topsSSE(symbols='AAPL', on_data=print_data)
