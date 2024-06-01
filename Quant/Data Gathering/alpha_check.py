from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt


key_path = "keys.txt"

# extracting data for a single ticker
ts = TimeSeries(key=open(key_path,'r').read(), output_format='pandas')

#ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
data['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()


from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key=open(key_path,'r').read())
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL')

print(data)
print(meta_data)