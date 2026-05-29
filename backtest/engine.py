import pandas as pd

def run_backtest(df: pd.DataFrame, initial_capital: float = 100000.0) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): DataFrame from compute_signals, containing Close and position
        initial_capital (float, optional): Starting cash in dollars. Defaults to 100000.0.

    Returns:
        pd.DataFrame with additional columns:
            - returns: daily % change in Close price
            - strategy: daily % return of the strategy (only on days we hold)
            - equity: portfolio value over time
            - benchmark: buy-and-hold equity curve for comparison
    """
    
    df = df.copy()
    df["returns"] = df["Close"].pct_change()
    df.dropna(inplace=True)
    df["strategy"] = df["returns"] * df["signal"].shift(1)
    df["equity"] = (1 + df["strategy"]).cumprod() * initial_capital
    df["benchmark"] = (1 + df["returns"]).cumprod() * initial_capital
    
    return df