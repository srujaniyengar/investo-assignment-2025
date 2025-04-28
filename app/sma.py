import pandas as pd
from sqlmodel import Session
from app.models import StockData

def calculate_sma(data, window):
    """Calculate Simple Moving Average."""
    return data.rolling(window=window).mean()

def moving_average_crossover_strategy(session: Session):
    """Implement the Moving Average Crossover Strategy."""
    # Fetch all stock data
    result = session.query(StockData).all()
    df = pd.DataFrame([{
        "datetime": record.datetime,
        "close": record.close
    } for record in result]).sort_values("datetime")

    # Calculate short-term and long-term moving averages
    df["short_term_sma"] = calculate_sma(df["close"], window=5)
    df["long_term_sma"] = calculate_sma(df["close"], window=20)

    # Generate buy/sell signals
    df["signal"] = 0
    df.loc[df["short_term_sma"] > df["long_term_sma"], "signal"] = 1  # Buy
    df.loc[df["short_term_sma"] <= df["long_term_sma"], "signal"] = -1  # Sell

    # Strategy performance (example: cumulative returns)
    df["strategy_returns"] = df["signal"].shift(1) * df["close"].pct_change()
    performance = df["strategy_returns"].cumsum().iloc[-1]

    return {
        "signals": df[["datetime", "signal"]].to_dict(orient="records"),
        "performance": performance
    }