from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class StockData(SQLModel, table=True):
    """Database model for stock data."""
    datetime: datetime = Field(primary_key=True)
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockDataCreate(SQLModel):
    """Pydantic model for input validation."""
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int