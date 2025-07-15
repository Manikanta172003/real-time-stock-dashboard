import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

async def fetch_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)

        # Get current price
        price = ticker.info.get("regularMarketPrice")
        previous_close = ticker.info.get("regularMarketPreviousClose", price)
        change = ((price - previous_close) / previous_close) * 100 if previous_close else 0

        volume = ticker.info.get("volume", 0)

        # Historical data (last day, 1-min interval)
        hist = ticker.history(period="1d", interval="1m")

        # Return dataframe, price, % change, volume
        return hist, price, change, volume

    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        print(f"⚠️ API error: {e}")
        return None, None, None, None
