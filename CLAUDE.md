# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (note: curl_cffi is required but missing from requirements.txt)
pip install streamlit yfinance plotly pandas curl_cffi

# Run the app
streamlit run app.py
```

## GitHub

Repositório: https://github.com/raul1791/b3-stocks-dashboard

**Auto-push ativo:** a cada arquivo salvo ou editado pelo Claude Code, o hook `PostToolUse` executa `autopush.ps1` automaticamente — faz `git add -A`, commit com timestamp e `git push origin master`. Não é necessário fazer push manualmente.

Para forçar push manual:
```powershell
powershell -ExecutionPolicy Bypass -File autopush.ps1
```

O hook está configurado em `.claude/settings.json`. Para desativar temporariamente, abra `/hooks` no Claude Code.

## Architecture

A single-page Streamlit dashboard for Brazilian B3 stocks (PETR4, VALE3, ITUB4) in 2025, structured across three modules:

- **`data.py`** — defines `TICKERS`, fetches OHLCV data via `yfinance` + `curl_cffi` (Chrome impersonation to bypass Yahoo Finance bot detection), caches results for 1 hour with `@st.cache_data(ttl=3600)`, and computes YTD summary metrics.
- **`charts.py`** — builds three Plotly figures (closing price, cumulative return %, daily volume) from a `dict[str, pd.DataFrame]` keyed by ticker symbol. Shares a `_LAYOUT` base and `_RANGE_SELECTOR` for consistent dark-theme styling.
- **`app.py`** — entry point: renders the sidebar selector, triggers data fetch, displays KPI metrics via `st.metric`, and routes charts into tabs.

### Key design points

- `TICKERS`, `COLORS`, and `LABELS` are duplicated between `data.py` and `charts.py` and must be kept in sync when adding new tickers.
- `fetch_stock_data` returns `dict[str, pd.DataFrame]`; all chart builders and `get_summary` expect this shape.
- `curl_cffi` is used in `data.py` (`_session()`) but is **not listed in `requirements.txt`** — it must be installed separately.
- The "Atualizar dados" sidebar button calls `st.cache_data.clear()` to force a fresh fetch.
