#!/usr/bin/env python3
"""
fetch_market_data.py
Runs via GitHub Actions on a schedule.
Fetches global market data using yfinance and writes data.json to repo root.
"""
import json, datetime, sys

try:
    import yfinance as yf
except ImportError:
    print("yfinance not installed, installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

SYMBOLS = {
    'sp':     '^GSPC',
    'ndq':    '^IXIC',
    'dji':    '^DJI',
    'inr':    'INR=X',
    'crude':  'CL=F',
    'gold':   'GC=F',
    'silver': 'SI=F',
    'n50':    '^NSEI',
    'bn':     '^NSEBANK',
    'sx':     '^BSESN',
    'fn':     'NIFTY_FIN_SERVICE.NS',
    'vix':    '^INDIAVIX',
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
                'price': round(float(price), 2),
                'chgPct': round(float(chg_pct), 2),
                'src': 'GHA'
            }
            print(f"[OK] {key} ({sym}): {price:.2f} ({chg_pct:+.2f}%)")
        else:
            errors.append(f"{key}: no price data")
            print(f"[SKIP] {key} ({sym}): price={price}, prev={prev}")
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

print(f"\nWrote data.json with {len(data)} symbols")
print(json.dumps(output, indent=2))
