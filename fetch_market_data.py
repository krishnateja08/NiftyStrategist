#!/usr/bin/env python3
"""
fetch_market_data.py
Runs via GitHub Actions every 15 min.
Fetches global indices + Nifty Top 10 stocks via yfinance → writes data.json
"""
import json, datetime, sys

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

SYMBOLS = {
    # Global indices & commodities
    'sp':     '^GSPC',
    'ndq':    '^IXIC',
    'dji':    '^DJI',
    'inr':    'INR=X',
    'crude':  'CL=F',
    'gold':   'GC=F',
    'silver': 'SI=F',
    # Indian indices
    'n50':    '^NSEI',
    'bn':     '^NSEBANK',
    'sx':     '^BSESN',
    'fn':     'NIFTY_FIN_SERVICE.NS',
    'vix':    '^INDIAVIX',
    # Nifty Top 10 stocks
    't_RELIANCE':   'RELIANCE.NS',
    't_HDFCBANK':   'HDFCBANK.NS',
    't_ICICIBANK':  'ICICIBANK.NS',
    't_INFY':       'INFY.NS',
    't_TCS':        'TCS.NS',
    't_AIRTEL':     'BHARTIARTL.NS',
    't_ITC':        'ITC.NS',
    't_SBI':        'SBIN.NS',
    't_KOTAK':      'KOTAKBANK.NS',
    't_LT':         'LT.NS',
    # US Top 10 stocks (by market cap)
    'u_AAPL':   'AAPL',
    'u_MSFT':   'MSFT',
    'u_NVDA':   'NVDA',
    'u_AMZN':   'AMZN',
    'u_GOOGL':  'GOOGL',
    'u_META':   'META',
    'u_TSLA':   'TSLA',
    'u_BRK':    'BRK-B',
    'u_JPM':    'JPM',
    'u_UNH':    'UNH',
}

data = {}
errors = []

for key, sym in SYMBOLS.items():
    try:
        ticker = yf.Ticker(sym)
        info = ticker.fast_info
        price = info.last_price
        prev  = info.previous_close
        if price and prev and prev > 0:
            chg_pct = ((price - prev) / prev) * 100
            data[key] = {
                'price':  round(float(price), 2),
                'chgPct': round(float(chg_pct), 2),
                'src':    'GHA'
            }
            print(f"[OK] {key} ({sym}): {price:.2f} ({chg_pct:+.2f}%)")
        else:
            errors.append(f"{key}: no price")
            print(f"[SKIP] {key}: price={price}, prev={prev}")
    except Exception as e:
        errors.append(f"{key}: {e}")
        print(f"[ERR] {key} ({sym}): {e}")

output = {
    'updated': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'data': data,
    'errors': errors
}

with open('data.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nWrote data.json — {len(data)} symbols, {len(errors)} errors")
