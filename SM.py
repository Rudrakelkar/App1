import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.main{
    background:#0E1117;
}
.stMetric{
    background:#161B22;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 Global Stock Dashboard")
st.write("Track stocks from Yahoo Finance in real time.")

stocks = {
    "Apple":"AAPL",
    "Microsoft":"MSFT",
    "Google":"GOOGL",
    "Amazon":"AMZN",
    "Tesla":"TSLA",
    "NVIDIA":"NVDA",
    "Meta":"META",
    "Netflix":"NFLX",
    "Reliance":"RELIANCE.NS",
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS",
    "HDFC Bank":"HDFCBANK.NS",
    "ICICI Bank":"ICICIBANK.NS"
}

st.sidebar.title("Select Stock")

company = st.sidebar.selectbox(
    "Popular Stocks",
    list(stocks.keys())
)

ticker = st.sidebar.text_input(
    "Or Enter Ticker",
    stocks[company]
)

period = st.sidebar.selectbox(
    "Chart Period",
    ["1d","5d","1mo","3mo","6mo","1y","5y","max"]
)

intervals = {
    "1d":"5m",
    "5d":"15m",
    "1mo":"1h",
    "3mo":"1d",
    "6mo":"1d",
    "1y":"1d",
    "5y":"1wk",
    "max":"1mo"
}

stock = yf.Ticker(ticker)

info = stock.info

hist = stock.history(
    period=period,
    interval=intervals[period]
)

price = info.get("currentPrice")
previous = info.get("previousClose")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Current Price", f"${price}")
col2.metric("Previous Close", f"${previous}")
col3.metric("Open", info.get("open"))
col4.metric("Volume", info.get("volume"))

col5,col6,col7,col8 = st.columns(4)

col5.metric("Day High", info.get("dayHigh"))
col6.metric("Day Low", info.get("dayLow"))
col7.metric("Market Cap", f"{info.get('marketCap'):,}")
col8.metric("52W High", info.get("fiftyTwoWeekHigh"))

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        line=dict(width=3),
        name="Close Price"
    )
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    title=f"{ticker} Price Chart",
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Company Information")

st.write(info.get("longBusinessSummary","No description available."))

st.subheader("Recent Data")

st.dataframe(hist.tail(20), use_container_width=True)
