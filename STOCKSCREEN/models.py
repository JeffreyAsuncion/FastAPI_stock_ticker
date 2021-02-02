from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric

# this is for multiple table and relationships
from sqlalchemy.orm import relationship

# this is the Base in database.py
from database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2)) # 10 places before . and 2 after
    forward_pe = Column(Numeric(10, 2)) 
    forward_eps = Column(Numeric(10, 2)) 
    dividend_yield = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2)) 
    ma200 = Column(Numeric(10, 2)) 
