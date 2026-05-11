import pandas as pd
import plotly.graph_objects as go

COLORS = {
    "PETR4.SA": "#00B4D8",
    "VALE3.SA": "#90E0EF",
    "ITUB4.SA": "#F4A261",
}

LABELS = {
    "PETR4.SA": "Petrobras (PETR4)",
    "VALE3.SA": "Vale (VALE3)",
    "ITUB4.SA": "Itaú (ITUB4)",
}

_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(14,17,23,1)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=20, t=60, b=40),
    hovermode="x unified",
)

_RANGE_SELECTOR = dict(
    buttons=[
        dict(count=1, label="1M", step="month", stepmode="backward"),
        dict(count=3, label="3M", step="month", stepmode="backward"),
        dict(count=6, label="6M", step="month", stepmode="backward"),
        dict(step="year", label="2025", stepmode="todate"),
        dict(step="all", label="Tudo"),
    ]
)


def build_closing_price_chart(data_dict: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    for ticker, df in data_dict.items():
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            name=LABELS.get(ticker, ticker),
            line=dict(color=COLORS.get(ticker), width=2),
            hovertemplate="%{y:.2f} R$<extra>" + LABELS.get(ticker, ticker) + "</extra>",
        ))
    fig.update_layout(
        **_LAYOUT,
        title="Preço de Fechamento Diário (R$)",
        xaxis=dict(rangeselector=_RANGE_SELECTOR, rangeslider=dict(visible=True), type="date"),
        yaxis=dict(title="Preço (R$)", tickprefix="R$ "),
    )
    return fig


def build_performance_chart(data_dict: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()

    fig.add_hline(y=0, line_dash="dash", line_color="grey", annotation_text="Baseline 0%")

    for ticker, df in data_dict.items():
        close = df["Close"]
        perf = (close / close.iloc[0] - 1) * 100
        fig.add_trace(go.Scatter(
            x=df.index,
            y=perf,
            name=LABELS.get(ticker, ticker),
            line=dict(color=COLORS.get(ticker), width=2),
            hovertemplate="%{y:.2f}%<extra>" + LABELS.get(ticker, ticker) + "</extra>",
        ))

    fig.update_layout(
        **_LAYOUT,
        title="Retorno Acumulado (%) desde Jan/2025",
        xaxis=dict(rangeselector=_RANGE_SELECTOR, rangeslider=dict(visible=True), type="date"),
        yaxis=dict(title="Retorno (%)", ticksuffix="%"),
    )
    return fig


def build_volume_chart(data_dict: dict[str, pd.DataFrame]) -> go.Figure:
    fig = go.Figure()
    for ticker, df in data_dict.items():
        fig.add_trace(go.Bar(
            x=df.index,
            y=df["Volume"],
            name=LABELS.get(ticker, ticker),
            marker_color=COLORS.get(ticker),
            hovertemplate="%{y:,.0f}<extra>" + LABELS.get(ticker, ticker) + "</extra>",
        ))
    fig.update_layout(
        **_LAYOUT,
        title="Volume Diário de Negociação",
        barmode="group",
        xaxis=dict(rangeselector=_RANGE_SELECTOR, type="date"),
        yaxis=dict(title="Volume", tickformat=".2s"),
    )
    return fig
