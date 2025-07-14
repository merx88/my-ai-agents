from crewai.tools import BaseTool
import requests

class CoingeckoTool(BaseTool):
    name: str = "CoingeckoTool"
    description: str = "Check Memecoin price/trading volume/market cap/volatility on CoinGecko"

    def _run(self, query: str) -> str:
        token = query.strip().lower()
        url = f"https://api.coingecko.com/api/v3/coins/{token}"
        r = requests.get(url)
        if r.status_code != 200:
            return f"Can'find '{token}'"
        d = r.json()
        m = d["market_data"]
        # return m
        return (
            f"💰 {d['name']} ({d['symbol'].upper()})\n"
            f"Price: ${m['current_price']['usd']}\n"
            f"market cap: ${m['market_cap']['usd']:,}\n"
            f"24h trading volume: ${m['total_volume']['usd']:,}\n"
            f"24h volatility: {m['price_change_percentage_24h']:.2f}%"
        )
