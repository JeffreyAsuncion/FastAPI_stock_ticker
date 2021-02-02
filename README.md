# FastAPI_stock_ticker https://www.youtube.com/watch?v=q8jaJ4Y3H7E
FastAPI - Stock Ticker - with Part Time Larry


# I am using pipenv
pipenv install fastapi
pipenv install uvicorn[standard]
pipenv install jinja2
pipenv install yfinance
pipenv install sqlalchemy

# if not using pipenv and using requirements.txt
# 'pip3 install -r requirements.txt'
# he uses 'venv/bin/activate' to activate his virtual environment
#   - then 'pip3 install -r requirements.txt'


# created main.py
# - get route
#   - check with web browser
# - post route
#   -  check with Client Postman




# ##################################################

# created templates folder
# - home.html
# - layout.html
# - import Requests


# add css and ui lib
# https://semantic-ui.com/ 
# - recipes
# find - CDN Releases
# -<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">

# - <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>
# add to layout.html

# back to getting started
# - need jquery
# Include in Your HTML


# want to add a table + standard input + checkbox + Button
# - semantic ui / collections / table
# - semantic ui / elements / standard input
# - semantic ui / modules / checkbox
# - semantic ui / Elements / Button - change class to primary to make blue


# ################################################


# SQLite
# FastAPI user guide - find SQL
# -  https://fastapi.tiangolo.com/tutorial/sql-databases/
# copy code - Import the SQLAlchemy parts

# tables aka models
# - Create the database models
#   - These classes are the SQLAlchemy models
# paste in models.py

# add __init__.py
# in models.py
#   - remove . : from .database import Base

# go back to main.py and link them to create table
#   - https://fastapi.tiangolo.com/tutorial/sql-databases/
#   -find create_all()
# paste - models.Base.metadata.create_all(bind=engine)
# under app = FastAPI
# add all imports
#    import models
#    from sqlalchemy.orm import Session
#    from database import SessionLocal, engine

# run app

# check out the db created

# go to folder where db is located
# sqlite3 stocks.db
# .schema


# ######################

# 1. Pydantic
#     define the structure of http requests
# 2. Dependency Injection
#    make sure that we have a database connection whenever an end point logic executes
# 3. Background Tasks
#   to fetch data in the background from yahoo finance


# 1. Pydantic - checking the types of data in and out
# ###########
#   'from pydantic import BaseModel'
# class & passing variables in the FUNCTION SIGNATURE
# automatic validation of every request 
#   passing and receiving the correct type int, str, float

# test with Postman - the post request
# Post / raw /json - 
# Learn more about Postman 
#           https://www.youtube.com/watch?v=eYQyqf-DtCQ
# JSON PAYLOAD
{"symbol":"APPL"} 
#   returns 
{
    "code": "success",
    "message": "stock"
}

# 2. Dependency Injection
# ######################
# before function executes 
#   make sure that there is a connection to the database
# import Depends 'from fastapi import FastAPI, Request, Depends'
# def get_db
def get_db():
    try: 
        db = SessionLocal()
        yield db
    finally:
        db.close()

# add a dependancy
# to def create_stock - db: Session = Depends(get_db) # must be at the end

# from models import Stock
# stock = Stock in def create stock

# Postman
{"symbol":"MSFT"}

# now check database and see if it posted
# >>> sqlite3 stocks.db
# SQLite version 3.31.1 2020-01-27 19:55:54
# Enter ".help" for usage hints.
# sqlite> select * from stocks;
# 1|MSFT||||||
# 2|APPL||||||
# sqlite>

# now our Object Relational Mapper is Working
# BIG WORDS for our class and db and fastapi are behaving nicely :-)

# using a dependency to get a database connection and we are injecting that to this function
# and we can access our database and insert 

# Delete and clean the test records
sqlite> delete from stocks;
sqlite> select * from stocks;
sqlite>


# 3. Background Tasks
# ###################
# next feature is main feature of our application
#   which is the part that actually fetches the key statistics from Yahoo Finance

# import BackgroundTasks
from fastapi import FastAPI, Request, Depends, BackgroundTasks

# the Depends needs to be at the end 
# so insert the BackgroundTask in the middle
def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

# add
background_tasks.add_task()

# make 
def fetch_stock_data(id: int):
    pass

# make it work, in background_tasks
background_tasks.add_task(fetch_stock_data, stock.id)

# working
def fetch_stock_data(id: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id = id).first()

    stock.forward_pe = 10

    db.add(stock)
    db.commit()


# teesting in POSTMAN
{"symbol":"PG"}
# return
{
    "code": "success",
    "message": "stock"
}
# then check in sqlite3
sqlite> select * from stocks;
1|PG||10||||
sqlite>

# add async 
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):


# test postman again
{"symbol":"JNJ"}
# return
{
    "code": "success",
    "message": "stock"
}
# check sqlite3
sqlite> select * from stocks;
1|PG||10||||
2|JNJ||10||||
sqlite>



# import yahoo financial pkg
import yfinanace 
# see yfinanace - Pypi for documentation

testyfinance.py

import yfinance as yf

msft = yf.Ticker("MSFT")

#get stock inof
print(msft.info)
# output GOOD
{'zip': '98052-6399', 'sector': 'Technology', 'fullTimeEmployees': 163000, 'longBusinessSummary': 'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. Its Productivity and Business Processes segment offers Office, Exchange, SharePoint, Microsoft Teams, Office 365 Security and Compliance, and Skype for Business, as well as related Client Access Licenses (CAL); Skype, Outlook.com, OneDrive, and LinkedIn; and Dynamics 365, a set of cloud-based and on-premises business solutions for small and medium businesses, large organizations, and divisions of enterprises. Its Intelligent Cloud segment licenses SQL and Windows Servers, Visual Studio, System Center, and related CALs; GitHub that provides a collaboration platform and code hosting service for developers; and Azure, a cloud platform. It also offers support services and Microsoft consulting services to assist customers in developing, deploying, and managing Microsoft server and desktop solutions; and training and certification to developers and IT professionals on various Microsoft products. Its More Personal Computing segment provides Windows original equipment manufacturer (OEM) licensing and other non-volume licensing of the Windows operating system; Windows Commercial, such as volume licensing of the Windows operating system, Windows cloud services, and other Windows commercial offerings; patent licensing; Windows Internet of Things; and MSN advertising. It also offers Surface, PC accessories, PCs, tablets, gaming and entertainment consoles, and other devices; Gaming, including Xbox hardware, and Xbox content and services; video games and third-party video game royalties; and Search, including Bing and Microsoft advertising. It sells its products through OEMs, distributors, and resellers; and directly through digital marketplaces, online stores, and retail stores. It has a strategic collaboration with DXC Technology. The company was founded in 1975 and is headquartered in Redmond, Washington.', 'city': 'Redmond', 'phone': '425-882-8080', 'state': 'WA', 'country': 'United States', 'companyOfficers': [], 'website': 'http://www.microsoft.com', 'maxAge': 1, 'address1': 'One Microsoft Way', 'industry': 'Software—Infrastructure', 'previousClose': 231.96, 'regularMarketOpen': 235.06, 'twoHundredDayAverage': 214.06598, 'trailingAnnualDividendYield': 0.009225729, 'payoutRatio': 0.31149998, 'volume24Hr': None, 'regularMarketDayHigh': 242.5, 'navPrice': None, 'averageDailyVolume10Day': 45657516, 'totalAssets': None, 'regularMarketPreviousClose': 231.96, 'fiftyDayAverage': 221.45813, 'trailingAnnualDividendRate': 2.14, 'open': 235.06, 'toCurrency': None, 'averageVolume10days': 45657516, 'expireDate': None, 'yield': None, 'algorithm': None, 'dividendRate': 2.24, 'exDividendDate': 1613520000, 'beta': 0.826155, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 232.46, 'priceHint': 2, 'currency': 'USD', 'trailingPE': 35.731327, 'regularMarketVolume': 31762797, 'lastMarket': None, 'maxSupply': None, 'openInterest': None, 'marketCap': 1807492972544, 'volumeAllCurrencies': None, 'strikePrice': None, 'averageVolume': 29775703, 'priceToSalesTrailing12Months': 11.791791, 'dayLow': 232.46, 'ask': 240.42, 'ytdReturn': None, 'askSize': 800, 'volume': 31762797, 'fiftyTwoWeekHigh': 242.64, 'forwardPE': 29.62299, 'fromCurrency': None, 'fiveYearAvgDividendYield': 1.71, 'fiftyTwoWeekLow': 132.52, 'bid': 240.05, 'tradeable': False, 'dividendYield': 0.0097, 'bidSize': 800, 'dayHigh': 242.5, 'exchange': 'NMS', 'shortName': 'Microsoft Corporation', 'longName': 'Microsoft Corporation', 'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EST', 'isEsgPopulated': False, 'gmtOffSetMilliseconds': '-18000000', 'quoteType': 'EQUITY', 'symbol': 'MSFT', 'messageBoardId': 'finmb_21835', 'market': 'us_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 11.092, 'beta3Year': None, 'profitMargins': 0.33473998, 'enterpriseToEbitda': 23.718, '52WeekChange': 0.3301984, 'morningStarRiskRating': None, 'forwardEps': 8.09, 'revenueQuarterlyGrowth': None, 'sharesOutstanding': 7560500224, 'fundInceptionDate': None, 'annualReportExpenseRatio': None, 'bookValue': 17.259, 'sharesShort': 41952779, 'sharesPercentSharesOut': 0.0056, 'fundFamily': None, 'lastFiscalYearEnd': 1593475200, 'heldPercentInstitutions': 0.71844, 'netIncomeToCommon': 51309998080, 'trailingEps': 6.707, 'lastDividendValue': 0.56, 'SandP52WeekChange': 0.14322305, 'priceToBook': 13.885508, 'heldPercentInsiders': 0.00059, 'nextFiscalYearEnd': 1656547200, 'mostRecentQuarter': 1609372800, 'shortRatio': 1.54, 'sharesShortPreviousMonthDate': 1607990400, 'floatShares': 7431722306, 'enterpriseValue': 1700285382656, 'threeYearAverageReturn': None, 'lastSplitDate': 1045526400, 'lastSplitFactor': '2:1', 'legalType': None, 'lastDividendDate': 1605657600, 'morningStarOverallRating': None, 'earningsQuarterlyGrowth': 0.327, 'dateShortInterest': 1610668800, 'pegRatio': 1.82, 'lastCapGain': None, 'shortPercentOfFloat': 0.0056, 'sharesShortPriorMonth': 39913925, 'impliedSharesOutstanding': None, 'category': None, 'fiveYearAverageReturn': None, 'regularMarketPrice': 235.06, 'logo_url': 'https://logo.clearbit.com/microsoft.com'}


# delete - stock.forward_pe = 10 from fetch_stock data 
# insert
    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    if yahoo_data.info['dividendYield'] is not None:
        stock.dividend_yield = yahoo_data.info['dividendYield'] * 100 


# Test it 
# check background test
# run web app
# postman test 
{"symbol":"AMZN"}
# return 
{
    "code": "success",
    "message": "stock"
}
# check sqlite3
sqlite> select * from stocks;
1|PG||10||||
2|JNJ||10||||
3|AMZN|3206.2|73.21244|45.66||3210.0344|3185.174
sqlite>

# video recap at 17:44 https://www.youtube.com/watch?v=ESVwKQLldjg
# TAKE NOTES OF THE PRESENTATION



# video part #5 - https://www.youtube.com/watch?v=xi96vi5X_Ak