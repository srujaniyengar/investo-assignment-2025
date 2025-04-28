import os
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime as datetime_type
from typing import Annotated, List
import pandas as pd

# Define the database model for ticker data
class TickerData(SQLModel, table=True):
    datetime: datetime_type = Field(primary_key=True)
    open: float
    high: float
    low: float
    close: float
    volume: int
    instrument: str

# Define the response model for strategy performance
class StrategyPerformance(SQLModel):
    total_return: float
    number_of_trades: int
    buy_signals: int
    sell_signals: int

# Retrieve database connection parameters from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Ensure all required environment variables are set
if not all([DB_NAME, DB_USERNAME, DB_PASSWORD]):
    raise Exception("Missing database parameters. Ensure DB_NAME, DB_USERNAME, and DB_PASSWORD are set in the environment.")

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to provide a database session
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Initialize the FastAPI app
app = FastAPI()

# Event to create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Endpoint to retrieve all ticker data
@app.get("/data", response_model=List[TickerData])
def read_data(session: SessionDep) -> List[TickerData]:
    return session.exec(select(TickerData)).all()

# Endpoint to add a new ticker data entry
@app.post("/data", response_model=TickerData)
def create_data(data: TickerData, session: SessionDep) -> TickerData:
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

# Endpoint to calculate strategy performance
@app.get("/strategy/performance", response_model=StrategyPerformance)
def calculate_performance(session: SessionDep) -> StrategyPerformance:
    # Query to fetch datetime and close price, sorted by datetime
    query = select(TickerData.datetime, TickerData.close).order_by(TickerData.datetime)
    datas = session.exec(query).all()

    # Debugging log to check the number of rows retrieved
    print(f"Number of rows retrieved: {len(datas)}")

    # Check if there is enough data for the performance calculation
    if len(datas) < 100:
        raise HTTPException(status_code=400, detail=f"Insufficient data: Only {len(datas)} rows available, 100 required.")

    # Convert the data into a pandas DataFrame for analysis
    df = pd.DataFrame(datas, columns=["datetime", "close"])
    df.set_index("datetime", inplace=True)

    # Calculate moving averages
    short_window, long_window = 20, 100
    df["short_ma"] = df["close"].rolling(window=short_window).mean()
    df["long_ma"] = df["close"].rolling(window=long_window).mean()

    # Generate buy/sell signals
    df["signal"] = 0
    df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1  # Buy signal
    df.loc[df["short_ma"] <= df["long_ma"], "signal"] = -1  # Sell signal

    # Calculate performance metrics
    total_return = (df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0]
    buy_signals = (df["signal"] == 1).sum()
    sell_signals = (df["signal"] == -1).sum()
    number_of_trades = buy_signals + sell_signals

    # Return the performance metrics
    return StrategyPerformance(
        total_return=total_return,
        number_of_trades=number_of_trades,
        buy_signals=buy_signals,
        sell_signals=sell_signals,
    )