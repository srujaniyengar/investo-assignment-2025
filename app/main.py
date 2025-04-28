from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.db import get_session
from app.crud import get_all_records, add_record
from app.models import StockDataCreate
from app.sma import moving_average_crossover_strategy

app = FastAPI()

@app.get("/data")
def fetch_data(session: Session = Depends(get_session)):
    """Fetch all records from the database."""
    return get_all_records(session)

@app.post("/data")
def insert_data(stock_data: StockDataCreate, session: Session = Depends(get_session)):
    """Add new records to the database."""
    return add_record(session, stock_data)

@app.get("/strategy/performance")
def strategy_performance(session: Session = Depends(get_session)):
    """Get performance of the Moving Average Crossover Strategy."""
    return moving_average_crossover_strategy(session)