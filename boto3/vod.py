import yfinance as yf

msft = yf.Ticker("AAPL")

# get stock info
print(msft.info)

# get historical market data
hist = msft.history(period="5d")

data_df = yf.download("AAPL", start="2020-01-01", end="2020-09-01")
data_df.to_csv('vod.csv')
