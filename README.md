# 📈 Financial Dashboard - Stock Candlestick Viewer

An interactive Tkinter application that visualizes **stock market data** using custom-drawn **candlestick charts**. Users can choose ticker symbols, select exchange types, and define date ranges to explore stock price movement with high-quality visuals.

---

## 🧠 Features

- Fetches real-time stock data using **Yahoo Finance (yfinance)**
- Renders detailed **candlestick charts** using `matplotlib`
- Input fields for:
  - Stock ticker
  - Exchange (NASDAQ, NSE, BSE, or None)
  - Start and end dates
- Fully themed dark UI
- Handles errors like:
  - Invalid date formats
  - No data available
  - Empty inputs

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Tkinter** – GUI
- **yfinance** – Stock data API
- **matplotlib** – Charting
- **datetime** – Date parsing and validation

---
## 📌 Notes

- Default ticker: `AAPL` (Apple Inc.)
- Default exchange: `NASDAQ`
- 📢 **Important:**  
  When using **Indian stocks** like `TCS`, `INFY`, `HDFCBANK`, etc.:
  - Use `NSE` for `.NS` tickers (e.g., `TCS.NS`)
  - Use `BSE` for `.BO` tickers (e.g., `TCS.BO`)
  - Use `NASDAQ` or `None` for US stocks (e.g., `AAPL`, `GOOGL`)
- Date format must be: `YYYY-MM-DD`
- Make sure you're connected to the internet to fetch stock data
