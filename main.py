from data.fetcher import fetch_ohlcv
from strategy.signals import compute_signals
from backtest.engine import run_backtest
from metrics.performance import compute_metrics

aapl_data = fetch_ohlcv("aapl", "2021-11-9", "2026-05-28")
signals = compute_signals(aapl_data)
backtest = run_backtest(signals)
metrics = compute_metrics(backtest)

print(metrics)