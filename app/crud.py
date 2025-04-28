from sqlmodel import Session
from app.models import StockData, StockDataCreate

def get_all_records(session: Session):
    """Fetch all records from the database."""
    return session.query(StockData).all()

def add_record(session: Session, stock_data: StockDataCreate):
    """Add a new record to the database."""
    new_record = StockData(**stock_data.dict())
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return new_record