# 📈 Real-Time Stock Dashboard

This is an interactive Python desktop application that shows real-time stock prices and charts using **Tkinter**, **Matplotlib**, and **Yahoo Finance data (yfinance)**.  

---

#Features

-  Add stocks using ticker symbols (e.g., AAPL, TSLA).
-  Select stocks from a dropdown list (no need to type manually).
-  Live price updates and automatic refresh every few seconds.
-  Plot price charts with moving average (MA) lines.
-  Highlight maximum and minimum points on the graph.
-  Export historical price data to CSV and Excel files.
-  Toggle between light and dark theme.
-  Remove individual stocks or clear all at once.

---

 Technologies Used

- Python 3.x
- Tkinter (GUI)
- Matplotlib (charting)
- yfinance (data)
- Pandas (data handling)

---

## ⚙️ How to Run Locally

1️⃣ Clone the repository:

```bash
git clone https://github.com/yourusername/real-time-stock-dashboard.git
2️⃣ Navigate to the project directory:

bash
Copy
Edit
cd real-time-stock-dashboard
3️⃣ Install required packages:

bash
Copy
Edit
pip install -r requirements.txt

4️⃣ Run the app:

bash
Copy
Edit
python gui.py
💡 Usage
Select a stock from the dropdown list or enter the ticker symbol manually.

Watch real-time updates and price movements.

Save historical data from the data folder (CSV format) or export to Excel (exports folder).

🗑️ Remove or Clear
Use the "Remove" button below each stock to remove it.

Use "Clear All" button to remove all stocks and clean charts.
