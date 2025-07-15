import sys
import os

# 👇 Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api import fetch_stock_data
import pytest

@pytest.mark.asyncio
async def test_fetch_stock_data():
    df, price, change, volume = await fetch_stock_data("AAPL")

    print(f"DataFrame: {df}")
    print(f"Price: {price}")
    print(f"Change: {change}")
    print(f"Volume: {volume}")

    assert df is not None, "DataFrame is None (API might have failed)"
    assert price is not None, "Price is None"
    assert change is not None, "Change is None"
    assert volume is not None, "Volume is None"
    print("✅ API test passed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_fetch_stock_data())
