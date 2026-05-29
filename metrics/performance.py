import pandas as pd
import numpy as np

def compute_metrics(df: pd.DataFrame, initial_capital: float = 100000.0) -> dict:
    """
    Args:
        df (pd.DataFrame): DataFrame from run_backtest, containin equity, strategy, returns columns
        initial_capital (float, optional): Starting capital, needed for drawdown and CAGR calculation. Defaults to 100000.0.

    Returns:
        dict with the following keys:
            - cagr : Compound Annual Growth Rate
            - sharpe_ratio : Risk-adjusted return (annualized)
            - max_drawdown : Largest peak-to-trough drop in equity
            - win_rate : % of trading days with positive strategy returns
            - total_return : overall % gain/loss over the period
    """
    
    metrics = dict()
    final_equity = df["equity"].iloc[-1]
    years = (df.index[-1] - df.index[0]).days / 365
    active = df[df["signal"] == 1]
    trade = df[df["position"] != 0]
    
    metrics["total_return"] = (final_equity - initial_capital) / initial_capital
    metrics["cagr"] = (final_equity / initial_capital) ** (1/years) - 1
    metrics["sharpe_ratio"] = active["strategy"].mean() / active["strategy"].std() * np.sqrt(252)
    metrics["max_drawdown"] = max(1 - df["equity"] / df["equity"].cummax())
    metrics["win_rate"] = len(trade[trade["strategy"] > 0]) / len(trade)
    
    return metrics
    