import streamlit as st

from data import TICKERS, START_DATE, fetch_stock_data, get_summary, today
from charts import build_closing_price_chart, build_performance_chart, build_volume_chart

st.set_page_config(
    page_title="Dashboard B3 2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
with st.sidebar:
    st.title("📈 Dashboard B3 2025")
    st.markdown("Análise de ações brasileiras ao longo de 2025.")

    selected = st.multiselect(
        "Selecione as ações",
        options=list(TICKERS.keys()),
        default=list(TICKERS.keys()),
        format_func=lambda t: TICKERS[t],
    )

    st.divider()

    if st.button("🔄 Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.caption(f"Dados de {START_DATE} até hoje")

# --- Guard ---
if not selected:
    st.warning("Selecione pelo menos uma ação na barra lateral.")
    st.stop()

# --- Data ---
with st.spinner("Buscando dados do Yahoo Finance..."):
    try:
        data = fetch_stock_data(selected, START_DATE, today())
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        st.stop()

# --- KPIs ---
cols = st.columns(len(selected))
for col, ticker in zip(cols, selected):
    summary = get_summary(data[ticker])
    col.metric(
        label=TICKERS[ticker],
        value=f"R$ {summary['latest_price']:.2f}",
        delta=f"{summary['ytd_return']:.1f}% YTD",
    )

st.divider()

# --- Charts ---
tab1, tab2, tab3 = st.tabs(["Preço de Fechamento", "Performance (%)", "Volume"])

with tab1:
    st.plotly_chart(build_closing_price_chart(data), use_container_width=True)

with tab2:
    st.plotly_chart(build_performance_chart(data), use_container_width=True)

with tab3:
    st.plotly_chart(build_volume_chart(data), use_container_width=True)

# --- Raw data ---
with st.expander("Ver dados brutos"):
    for ticker in selected:
        st.markdown(f"**{TICKERS[ticker]}**")
        df = data[ticker][["Open", "High", "Low", "Close", "Volume"]].copy()
        df["Close"] = df["Close"].map("R$ {:.2f}".format)
        df["Volume"] = df["Volume"].map("{:,.0f}".format)
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

st.caption("Fonte: Yahoo Finance via yfinance | Preços em BRL (R$) | Cache de 1 hora")
