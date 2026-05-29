import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_dashboard(df: pd.DataFrame, metrics: dict, ticker: str) -> None:
    """
    Args:
        df (pd.DataFrame): DataFrame from run_backtest, containing all columns
        metrics (dict): dict from compute_metrics
        ticker (str): stock symbol, used for chart titles
        
    Displays a Plotly dashboard with 3 panels:
        1. Price chart with short_ma, long_ma overlaid + buy/sell markers
        2. Equity curve vs benchmark
        3. Metrics summary table
    """
    fig = make_subplots(rows=3, cols=1, specs=[
        [{"type": "xy"}],    # row 1 - price chart
        [{"type": "xy"}],    # row 2 - equity curve
        [{"type": "table"}]  # row 3 - metrics table
    ])
    
    ### Panel 1
    fig.add_trace(
        go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close Price"), row=1, col=1 
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df["short_ma"], mode="lines", name="Short MA"), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df["long_ma"], mode="lines", name="Long MA"), row=1, col=1
    )

    buy = df[df["position"]==1]
    sell = df[df["position"]==-1]
    fig.add_trace(
        go.Scatter(x=buy.index, y=buy["Close"], mode="markers", marker_symbol="triangle-up", name="buy", marker=dict(color="green", size=10)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=sell.index, y=sell["Close"], mode="markers", marker_symbol="triangle-down", name="sell", marker=dict(color="red", size=10)),
        row=1, col=1
    )
    
    ### Panel 2
    fig.add_trace(
        go.Scatter(x=df.index, y=df["equity"], mode="lines", name="Equity"), row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df.index, y=df["benchmark"], mode="lines", name="Benchmark"), row=2, col=1
    )
    
    ### Panel 3
    metric_names = list(metrics.keys())
    metric_values = [f"{v:.2%}" if k != "sharpe_ratio" else f"{v:.2f}" for k, v in metrics.items()]
    fig.add_trace(
        go.Table(header=dict(values=["Metric", "Value"]), cells=dict(values=[metric_names, metric_values])),
        row=3, col=1)
    
    fig.show()
    