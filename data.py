import datetime
import pandas as pd
import streamlit as st
import yfinance as yf
from curl_cffi import requests as curl_req

TICKERS = {
    "PETR4.SA": "Petrobras (PETR4)",
    "VALE3.SA": "Vale (VALE3)",
    "ITUB4.SA": "Itaú (ITUB4)",
}

START_DATE = "2025-01-01"


def _session() -> curl_req.Session:
    return curl_req.Session(verify=False, impersonate="chrome")


@st.cache_data(ttl=3600)
def fetch_stock_data(tickers: list[str], start: str, end: str) -> dict[str, pd.DataFrame]:
    result = {}
    session = _session()
    for ticker in tickers:
        t = yf.Ticker(ticker, session=session)
        raw = t.history(start=start, end=end, auto_adjust=True)
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        df = raw.dropna(subset=["Close"])
        result[ticker] = df
    return result


def get_summary(df: pd.DataFrame) -> dict:
    close = df["Close"]
    latest = float(close.iloc[-1])
    first = float(close.iloc[0])
    ytd_return = (latest / first - 1) * 100
    avg_volume = float(df["Volume"].mean())
    return {
        "latest_price": latest,
        "ytd_return": ytd_return,
        "avg_volume": avg_volume,
        "last_date": df.index[-1],
    }


def today() -> str:
    return datetime.date.today().isoformat()
