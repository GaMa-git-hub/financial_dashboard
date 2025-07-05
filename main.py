import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CandlestickChart:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Candlestick Chart")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")

        plt.style.use('dark_background')

        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Stock Ticker:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=0, padx=5)
        self.ticker_var = tk.StringVar(value="AAPL")
        tk.Entry(control_frame, textvariable=self.ticker_var, width=10, font=("Arial", 12), bg="#404040", fg="white", insertbackground="white").grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Exchange:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=2, padx=5)
        self.exchange_var = tk.StringVar(value="NASDAQ")
        exchange_menu = ttk.Combobox(control_frame, textvariable=self.exchange_var, values=["NASDAQ", "NSE", "BSE", "None"], width=10, state="readonly")
        exchange_menu.grid(row=0, column=3, padx=5)

        tk.Label(control_frame, text="Start Date:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=4, padx=5)
        self.start_var = tk.StringVar(value="2023-01-01")
        tk.Entry(control_frame, textvariable=self.start_var, width=12, font=("Arial", 12), bg="#404040", fg="white", insertbackground="white").grid(row=0, column=5, padx=5)

        tk.Label(control_frame, text="End Date:", font=("Arial", 12), bg="#2b2b2b", fg="white").grid(row=0, column=6, padx=5)
        self.end_var = tk.StringVar(value="2024-01-01")
        tk.Entry(control_frame, textvariable=self.end_var, width=12, font=("Arial", 12), bg="#404040", fg="white", insertbackground="white").grid(row=0, column=7, padx=5)

        tk.Button(control_frame, text="Load Chart", command=self.load_chart, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20).grid(row=0, column=8, padx=10)

        chart_frame = tk.Frame(self.root, bg="#2b2b2b")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.load_chart()

    def load_chart(self):
        try:
            base_ticker = self.ticker_var.get().strip().upper()
            exchange = self.exchange_var.get()
            start_date_str = self.start_var.get().strip()
            end_date_str = self.end_var.get().strip()

            # Validate dates
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter dates in YYYY-MM-DD format.")
                return

            if start_date >= end_date:
                messagebox.showerror("Invalid Range", "Start date must be before end date.")
                return

            # Exchange suffix
            suffix_map = {"NSE": ".NS", "BSE": ".BO", "NASDAQ": "", "None": ""}
            suffix = suffix_map.get(exchange, "")
            ticker = base_ticker + suffix

            print(f"DEBUG: Fetching {ticker} from {start_date} to {end_date}")

            data = yf.download(ticker, start=start_date.isoformat(), end=end_date.isoformat(), progress=False, auto_adjust=True)

            if data.empty:
                messagebox.showerror("No Data", f"No data found for ticker '{ticker}' in the given range.")
                return

            self.create_candlestick_chart(data, ticker)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def create_candlestick_chart(self, data, ticker):
        try:
            self.ax.clear()

            dates = mdates.date2num(data.index.to_pydatetime())
            opens = data['Open'].values.flatten()
            highs = data['High'].values.flatten()
            lows = data['Low'].values.flatten()
            closes = data['Close'].values.flatten()

            up_days = closes >= opens
            down_days = closes < opens

            width = 0.6
            width2 = 0.05
            up_color = '#26a69a'
            down_color = '#ef5350'

            self.ax.bar(dates[up_days], closes[up_days] - opens[up_days], width, bottom=opens[up_days], color=up_color, alpha=0.8)
            self.ax.bar(dates[up_days], highs[up_days] - closes[up_days], width2, bottom=closes[up_days], color=up_color)
            self.ax.bar(dates[up_days], opens[up_days] - lows[up_days], width2, bottom=lows[up_days], color=up_color)

            self.ax.bar(dates[down_days], opens[down_days] - closes[down_days], width, bottom=closes[down_days], color=down_color, alpha=0.8)
            self.ax.bar(dates[down_days], highs[down_days] - opens[down_days], width2, bottom=opens[down_days], color=down_color)
            self.ax.bar(dates[down_days], closes[down_days] - lows[down_days], width2, bottom=lows[down_days], color=down_color)

            self.ax.set_title(f'{ticker} Stock Price', fontsize=16, fontweight='bold', pad=20)
            self.ax.set_ylabel('Price ($)', fontsize=12)
            self.ax.set_xlabel('Date', fontsize=12)
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())
            self.fig.autofmt_xdate()
            self.ax.grid(True, alpha=0.3)

            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Plot Error", f"Error drawing chart: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CandlestickChart(root)
    root.mainloop()
