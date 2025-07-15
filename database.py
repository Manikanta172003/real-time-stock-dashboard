from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine("sqlite:///stocks.db")
SessionLocal = sessionmaker(bind=engine)

class StockData(Base):
    __tablename__ = "stock_data"
    id = Column(String, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    change = Column(Float)
    volume = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

def save_stock_data(data):
    # Example placeholder implementation
    # Replace with actual database saving logic
    print(f"Saving stock data: {data}")
