import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import yfinance as yf
import pandas as pd
import os
from datetime import datetime
from tkinter import messagebox

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("exports", exist_ok=True)

# Theme
current_theme = {"bg": "white", "fg": "black"}

root = tk.Tk()
root.title("Real-Time Stock Dashboard")
root.geometry("900x600")
root.configure(bg=current_theme["bg"])

control_frame = tk.Frame(root, bg=current_theme["bg"])
control_frame.pack(pady=10)

# Entry for typing ticker symbol
entry = tk.Entry(control_frame, width=15)
entry.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(control_frame, text="Add Symbol", command=lambda: add_stock(entry.get().upper()))
add_button.pack(side=tk.LEFT, padx=5)

# Dropdown (Combobox) list
company_list = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Google (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
    "Meta (META)": "META",
    "NVIDIA (NVDA)": "NVDA",
    "Netflix (NFLX)": "NFLX",
    "Intel (INTC)": "INTC",
    "AMD (AMD)": "AMD"
}

combo = ttk.Combobox(control_frame, values=list(company_list.keys()), width=25)
combo.pack(side=tk.LEFT, padx=5)
combo.set("Select Company")

dropdown_button = tk.Button(control_frame, text="Add from List", command=lambda: add_stock(company_list.get(combo.get())))
dropdown_button.pack(side=tk.LEFT, padx=5)

theme_button = tk.Button(control_frame, text="Toggle Theme", command=lambda: toggle_theme())
theme_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(control_frame, text="Export to Excel", command=lambda: export_to_excel())
export_button.pack(side=tk.LEFT, padx=5)

clear_all_button = tk.Button(control_frame, text="Clear All", command=lambda: clear_all_stocks())
clear_all_button.pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, bg=current_theme["bg"])
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=current_theme["bg"])

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

stock_frames = {}

def fetch_data(symbol):
    try:
        data = yf.download(tickers=symbol, period="1d", interval="1m")
        if not data.empty:
            price = float(data["Close"].iloc[-1].item())
            return data, price
        else:
            return pd.DataFrame(), None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return pd.DataFrame(), None

def update_stock(symbol):
    hist, price = fetch_data(symbol)
    if not hist.empty and price is not None:
        ax = stock_frames[symbol]["ax"]
        ax.clear()
        ax.plot(hist.index, hist["Close"], label=f"{symbol} Price", color="blue")
        hist["MA5"] = hist["Close"].rolling(window=5).mean()
        ax.plot(hist.index, hist["MA5"], label="MA 5", linestyle="--", color="orange")
        max_idx = hist["Close"].idxmax()
        min_idx = hist["Close"].idxmin()
        ax.plot(max_idx, hist["Close"].max(), "ro", label="Max")
        ax.plot(min_idx, hist["Close"].min(), "go", label="Min")
        ax.set_title(f"{symbol} Live Price")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        stock_frames[symbol]["canvas"].draw()
        stock_frames[symbol]["price_label"].config(text=f"Current Price: ${price:.2f}")

        # Save data
        latest_row = hist.iloc[-1]
        close = float(latest_row["Close"].item())
        open_price = float(latest_row["Open"].item())
        volume = int(latest_row["Volume"].item())
        percent_change = ((close - open_price) / open_price) * 100
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = os.path.join("data", f"{symbol}.csv")
        with open(filename, "a") as f:
            f.write(f"{now},{close},{volume},{percent_change:.2f}\n")
    else:
        stock_frames[symbol]["price_label"].config(text="Error fetching data")

    stock_frames[symbol]["frame"].after(10000, lambda: update_stock(symbol))

def add_stock(symbol):
    if not symbol or symbol in stock_frames:
        return

    frame = tk.Frame(scrollable_frame, bd=2, relief="groove", bg=current_theme["bg"])
    frame.pack(pady=10, padx=10, fill="x")

    price_label = tk.Label(frame, text="Fetching...", bg=current_theme["bg"], fg=current_theme["fg"])
    price_label.pack()

    fig = Figure(figsize=(6, 2), dpi=100)
    ax = fig.add_subplot(111)

    canvas_widget = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()

    remove_button = tk.Button(frame, text="Remove", command=lambda sym=symbol: remove_stock(sym))
    remove_button.pack(pady=5)

    stock_frames[symbol] = {
        "frame": frame,
        "price_label": price_label,
        "fig": fig,
        "ax": ax,
        "canvas": canvas_widget
    }

    update_stock(symbol)

def remove_stock(symbol):
    if symbol in stock_frames:
        frame = stock_frames[symbol]["frame"]
        frame.destroy()
        del stock_frames[symbol]
        filename = os.path.join("data", f"{symbol}.csv")
        if os.path.exists(filename):
            os.remove(filename)
        print(f"{symbol} removed successfully.")

def clear_all_stocks():
    symbols = list(stock_frames.keys())
    for sym in symbols:
        remove_stock(sym)
    print("✅ All stocks cleared.")

def toggle_theme():
    if current_theme["bg"] == "white":
        new_bg, new_fg = "black", "white"
    else:
        new_bg, new_fg = "white", "black"

    root.configure(bg=new_bg)
    control_frame.configure(bg=new_bg)
    scrollable_frame.configure(bg=new_bg)
    entry.configure(bg=new_bg, fg=new_fg, insertbackground=new_fg)
    combo.configure(background=new_bg, foreground=new_fg)
    add_button.configure(bg=new_bg, fg=new_fg)
    dropdown_button.configure(bg=new_bg, fg=new_fg)
    theme_button.configure(bg=new_bg, fg=new_fg)
    export_button.configure(bg=new_bg, fg=new_fg)
    clear_all_button.configure(bg=new_bg, fg=new_fg)
    canvas.configure(bg=new_bg)

    for frames in stock_frames.values():
        frames["frame"].configure(bg=new_bg)
        frames["price_label"].configure(bg=new_bg, fg=new_fg)

    current_theme["bg"], current_theme["fg"] = new_bg, new_fg

def export_to_excel():
    for symbol in stock_frames.keys():
        csv_file = os.path.join("data", f"{symbol}.csv")
        excel_file = os.path.join("exports", f"{symbol}.xlsx")
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file, names=["Time", "Price", "Volume", "% Change"])
            df.to_excel(excel_file, index=False)
    print("✅ Exported to Excel files in 'exports' folder.")

# Default stock (optional)
# add_stock("AAPL")

root.mainloop()
