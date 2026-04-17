from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

# ✅ CREATE APP ONLY ONCE
app = FastAPI()

# ✅ CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sector mapping
symbol_map = {
    "technology": "AAPL",
    "healthcare": "JNJ",
    "finance": "JPM",
    "energy": "XOM",
    "agriculture": "ADM",
    "automobile": "TSLA"
}

@app.get("/analyze/{sector}")
def analyze_sector(sector: str):
    try:
        symbol = symbol_map.get(sector.lower(), "AAPL")

        data = yf.download(symbol, period="1y")

        if data.empty:
            return {"error": "No data found"}

        # -------- CLOSE --------
        close_series = data["Close"]

        if hasattr(close_series, "columns"):
            close_series = close_series.iloc[:, 0]

        close_series = close_series.dropna()

        # -------- RETURNS --------
        returns = close_series.pct_change().dropna()

        if len(returns) == 0:
            return {"error": "No returns data"}

        growth = float(returns.mean()) * 1000
        risk = float(returns.std()) * 1000

        # -------- VOLUME --------
        volume_series = data["Volume"]

        if hasattr(volume_series, "columns"):
            volume_series = volume_series.iloc[:, 0]

        volume_change = volume_series.pct_change().dropna()
        demand = float(volume_change.mean()) * 100 if len(volume_change) > 0 else 0

        # -------- NORMALIZE --------
        growth = int(max(0, min(100, growth)))
        risk = int(max(0, min(100, risk)))
        demand = int(max(0, min(100, demand)))

        # -------- TREND --------
        prices = close_series.values.tolist()[-30:]
        dates = close_series.index.strftime("%Y-%m-%d").tolist()[-30:]

        return {
            "growth": growth,
            "risk": risk,
            "demand": demand,
            "trend_prices": prices,
            "trend_dates": dates,
            "insights": [
                f"Stock: {symbol}",
                "Growth from price movement",
                "Risk from volatility",
                "Demand from volume activity"
            ]
        }

    except Exception as e:
        return {"error": str(e)}