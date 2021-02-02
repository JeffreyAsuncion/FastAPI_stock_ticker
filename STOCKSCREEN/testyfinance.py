import yfinance as yf

msft = yf.Ticker("MSFT")

#get stock inof
print(msft.info)
