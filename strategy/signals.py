import pandas as pd

def compute_signals(df: pd.DataFrame, short_window: int = 50, long_window: int = 200) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): OHLCV DataFrame from fetch_ohlcv
        short_window (int, optional): lookback period for short MA. Defaults to 50.
        long_window (int, optional): lookback period for long MA. Defaults to 200.

    Returns:
        pd.DataFrame with additional columns:
            - short_ma: short-term moving average of Close
            - long_ma: long-term moving average of Close
            - signal: 1 when short_ma > long_ma, else 0
            - position: daily change in signal (1 = buy, -1 = sell, 0 = hold)
    """
    if (short_window >= long_window):
        raise ValueError("short_window must be less than long_window")
    
    df = df.copy()
    
    df["short_ma"] = df["Close"].rolling(window=short_window).mean()
    df["long_ma"] = df["Close"].rolling(window=long_window).mean()
    
    df["signal"] = (df["short_ma"] > df["long_ma"]).astype(int)
    df["position"] = df["signal"].diff()
    df.dropna(inplace=True)
    return df