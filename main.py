from data.fetcher import fetch_ohlcv
from strategy.signals import compute_signals
from backtest.engine import run_backtest
from metrics.performance import compute_metrics
from dashboard.app import plot_dashboard
import argparse

def parse_args():
    
    parser = argparse.ArgumentParser(description="MA Crossover Backtest")
    
    parser.add_argument("--ticker", type=str, default="AAPL")
    parser.add_argument("--start", type=str, default="2021-11-9")
    parser.add_argument("--end", type=str, default="2026-05-28")
    parser.add_argument("--initial_capital", type=float, default=100000.0)
    parser.add_argument("--short_window", type=int, default=50)
    parser.add_argument("--long_window", type=int, default=200)
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    stock_data = fetch_ohlcv(args.ticker, args.start, args.end)
    signals = compute_signals(stock_data, args.short_window, args.long_window)
    backtest = run_backtest(signals, args.initial_capital)
    metrics = compute_metrics(backtest)
    plot_dashboard(backtest, metrics, args.ticker)

if __name__ == "__main__":
    main()