from langchain_core.tools import tool
import yfinance as yf
import pandas as pd


@tool
def fetch_fundamental_data(ticker: str):
    """Fetches key fundamental metrics like Price, P/E Ratio, and Market Cap."""
    # Auto-fix for Indian stocks
    search_ticker = f"{ticker}.NS" if ".NS" not in ticker and ".BO" not in ticker else ticker
    stock = yf.Ticker(search_ticker)
    info = stock.info

    price = info.get("currentPrice", 0)
    pe = info.get("trailingPE", 0)
    cap = info.get("marketCap", 0)

    return f"Ticker: {search_ticker} | Price: {price} | PE Ratio: {pe} | Market Cap: {cap}"


@tool
def get_advanced_tech_analysis(ticker: str):
    """
    Provides a definitive Bullish/Bearish verdict using SMA50, RSI, and Volume.
    """
    search_ticker = f"{ticker}.NS" if ".NS" not in ticker and ".BO" not in ticker else ticker

    # Fetch 1 year of data
    df = yf.download(search_ticker, period="1y", progress=False)

    if df.empty or len(df) < 50:
        return f"Error: Not enough historical data for {search_ticker}."

    # --- FIX: Ensure we are working with 1D Series for calculations ---
    # Sometimes yfinance returns a MultiIndex DataFrame; we select 'Close' specifically
    close_prices = df['Close'].squeeze()
    volume_data = df['Volume'].squeeze()

    # 1. SMA 50 Calculation
    sma50_series = close_prices.rolling(window=50).mean()

    # 2. RSI 14 Calculation
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))

    # 3. Volume Analysis
    vol_avg_series = volume_data.rolling(window=20).mean()

    # --- FIX: Use .iloc[-1] and force to float safely ---
    try:
        # We use .iloc[-1] and then cast to float.
        # If it's still a Series, .values[0] picks the first actual number.
        curr_price = float(close_prices.iloc[-1])
        sma50 = float(sma50_series.iloc[-1])
        rsi = float(rsi_series.iloc[-1])
        curr_vol = float(volume_data.iloc[-1])
        avg_vol = float(vol_avg_series.iloc[-1])

        # --- VERDICT LOGIC ---
        trend = "BULLISH" if curr_price > sma50 else "BEARISH"

        if rsi < 30:
            rsi_status = "OVERSOLD (Potential for a bounce)"
        elif rsi > 70:
            rsi_status = "OVERBOUGHT (Potential for a correction)"
        else:
            rsi_status = "NEUTRAL"

        vol_status = "High Volume" if curr_vol > (avg_vol * 1.5) else "Normal Volume"

        return (
            f"--- TECHNICAL VERDICT FOR {search_ticker} ---\n"
            f"Trend: {trend}\n"
            f"Price: {curr_price:.2f} | 50-DMA: {sma50:.2f}\n"
            f"RSI: {rsi:.2f} -> {rsi_status}\n"
            f"Volume: {vol_status}\n"
            f"Summary: The stock is {trend} and currently {rsi_status}."
        )
    except Exception as e:
        return f"Error extracting numeric values: {str(e)}"












# from langchain_core.tools import tool
# import yfinance as yf
#
#
# @tool
# def fetch_fundamental_data(ticker: str):
#     """Fetches fundamental metrics for a stock ticker."""
#     stock = yf.Ticker(ticker)
#     info = stock.info
#
#     # Use .get() with a fallback to avoid errors if a key is missing
#     price = info.get("currentPrice", 0)
#     pe = info.get("trailingPE", 0)
#     cap = info.get("marketCap", 0)
#
#     return f"Price: {price}, PE Ratio: {pe}, Market Cap: {cap}"
#
#
# @tool
# def get_technical_summary(ticker: str):
#     """
#     Calculates the 50-day moving average to determine trend.
#     Use this to see if a stock is 'Bullish' or 'Bearish'.
#     """
#     # 1. Fetch data
#     df = yf.download(ticker, period="60d", progress=False)
#
#     # 2. Calculate SMA
#     df['SMA50'] = df['Close'].rolling(window=50).mean()
#
#     # 3. Extract last values and force them to floats
#     # .iloc[-1] gets the last row, .item() ensures it's a single scalar
#     try:
#         curr = float(df['Close'].iloc[-1])
#         sma = float(df['SMA50'].iloc[-1])
#
#         status = 'Bullish' if curr > sma else 'Bearish'
#
#         # Now the formatting :.2f will work perfectly
#         return f"Price: {curr:.2f}, SMA50: {sma:.2f}. Trend: {status}"
#     except Exception as e:
#         return f"Error processing data for {ticker}: {str(e)}"