from crewai.tools import BaseTool
import requests
import json


class DexscreenerTool(BaseTool):
    name: str = "DexscreenerTool"
    description: str = (
        "Fetch bsc memecoin data from Dexscreener API (Get the pools of a given token address)"
    )

    def _run(self, address: str) -> str:
        try:
            url = f"https://api.dexscreener.com/token-pairs/v1/bsc/{address}"
            response = requests.get(url)
            data = response.json()

            result = []
            for pair in data:
                result.append(
                    {
                        "name": pair["baseToken"]["name"],
                        "symbol": pair["baseToken"]["symbol"],
                        "price_usd": pair["priceUsd"],
                        "market_cap": pair.get("marketCap"),
                        "volume_24h": pair["volume"]["h24"],
                        "liquidity_usd": pair["liquidity"]["usd"],
                        "price_change_24h": pair["priceChange"]["h24"],
                        "website": pair.get("info", {})
                        .get("websites", [{}])[0]
                        .get("url"),
                        "twitter": next(
                            (
                                s["url"]
                                for s in pair.get("info", {}).get("socials", [])
                                if s["type"] == "twitter"
                            ),
                            None,
                        ),
                        "telegram": next(
                            (
                                s["url"]
                                for s in pair.get("info", {}).get("socials", [])
                                if s["type"] == "telegram"
                            ),
                            None,
                        ),
                        "dex_url": pair.get("url"),
                    }
                )

            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {e}"
