import pandas as pd
import yfinance as yf
import os

def fetch_ohlcv(ticker: str, start: str, end: str, cache_dir: str = "data/cache") -> pd.DataFrame:
    """
    Args:
        ticker (str): stock symbol e.g. "AAPL"
        start (str): start date e.g. "2026-01-01"
        end (str): end date e.g. "2026-12-31"
        cache_dir (str, optional): folder to store cached files. Defaults to "data/cache".

    Returns:
        pd.DataFrame: dataframe with DateTimeIndex and columns: Open, High, Low, Close, Volume
    """
    
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = f"{cache_dir}/{ticker}_{start}_{end}.parquet"
    
    try:
        df = pd.read_parquet(cache_file)
    except FileNotFoundError:
        df = yf.download(ticker, start=start, end=end, multi_level_index=False)
        if df.empty:
            raise ValueError(f"No data found for ticker {ticker} between {start} and {end}. Check the ticker or data range")
        df.to_parquet(cache_file)
    
    return df