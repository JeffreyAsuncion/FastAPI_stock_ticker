import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from fastapi import FastAPI, Request, Depends, BackgroundTasks
# FastAPI is a framework to create apis and web apps
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from models import Stock
import yfinance

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# look for templates in the templates directory
templates = Jinja2Templates(directory="templates") 

class StockRequest(BaseModel):
    symbol: str

def get_db():
    try: 
        db = SessionLocal()
        yield db
    finally:
        db.close()

# you can test in the browser
@app.get("/") 
def home(request: Request):
    """
        Displays the stock screener dashboard / homepage
    """
    return templates.TemplateResponse("home.html", {
        "request": request,
    })


def fetch_stock_data(id: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()

    yahoo_data = yfinance.Ticker(stock.symbol)

    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    if yahoo_data.info['dividendYield'] is not None:
        stock.dividend_yield = yahoo_data.info['dividendYield'] * 100 

    db.add(stock)
    db.commit()

@app.post("/stock") # you need to test in a client like Postman or Insominia
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # this function depends on get_db
    """
        Creates a sstock and stores it in the database
    """

    # instantiate Stock class from model
    stock = Stock()
    # class stock symbol equals stock_request symbol
    stock.symbol = stock_request.symbol

    # db is SessionLocal which is like a cursor
    db.add(stock)
    db.commit()

    # id came from the just inserted stock above
    background_tasks.add_task(fetch_stock_data, stock.id)

    return {
        "code": "success",
        "message": "stock"
    }
