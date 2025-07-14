from crewai.tools import BaseTool
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BSCSCAN_BASE_URL = "https://api.etherscan.io/v2/api?chainid=56"
BSCSCAN_API_KEY = os.getenv("BSCSCAN_API_KEY")


class BscscanTool(BaseTool):
    name: str = "BscscanTool"
    description: str = (
        "Check token information, transaction, contract source code with bscscan api"
    )

    def _run(
        self,
        mode: str,
        address: str,
        contract_address: str = None,
        page: int = 1,
        offset: int = 5,
    ) -> str:

        try:
            address = address.strip().lower()
            if contract_address:
                contract_address = contract_address.strip().lower()

            if mode == "total_supply":
                url = f"{BSCSCAN_BASE_URL}&module=stats&action=tokensupply&contractaddress={address}&apikey={BSCSCAN_API_KEY}"
                resp = requests.get(url)
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") == "1":
                    supply = data.get("result")
                    return f"💎 total supply: {int(supply):,} (raw value)"
                return f"❗ Total supply lookup failed: {data.get('message')}"

            elif mode == "source_code":
                url = f"{BSCSCAN_BASE_URL}&module=contract&action=getsourcecode&address={address}&apikey={BSCSCAN_API_KEY}"
                resp = requests.get(url)
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") != "1":
                    return f"❗ Source code lookup failed: {data.get('message')}"
                contract_data = data["result"][0]
                contract_name = contract_data.get("ContractName", "N/A")
                source_code = contract_data.get("SourceCode", "N/A")
                abi = contract_data.get("ABI", "N/A")
                try:
                    abi_pretty = json.dumps(json.loads(abi), indent=2)
                except:
                    abi_pretty = abi
                return (
                    f"📜 Contract name: {contract_name}\n"
                    f"🔗 Contract source code:\n```solidity\n{source_code}\n```\n"
                    f"🤖 ABI:\n```json\n{abi_pretty}\n```"
                )

            elif mode == "normal_tx":
                url = (
                    f"{BSCSCAN_BASE_URL}&module=account&action=txlist&address={address}"
                    f"&startblock=0&endblock=99999999&page={page}&offset={offset}&sort=desc&apikey={BSCSCAN_API_KEY}"
                )
                resp = requests.get(url)
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") != "1":
                    return f"❗ Failed transaction lookup: {data.get('message')}"
                transactions = data.get("result", [])
                summary = []
                for tx in transactions:
                    summary.append(
                        f"- Hash: {tx.get('hash')[:10]}... | From: {tx.get('from')[:10]}... | To: {tx.get('to')[:10]}... | Value: {int(tx.get('value')) / 1e18:.4f} BNB"
                    )
                return f"📄 Recent general transaction history:\n" + "\n".join(summary)

            elif mode == "token_transfers":
                url = (
                    f"{BSCSCAN_BASE_URL}&module=account&action=tokentx&address={address}"
                    f"&startblock=0&endblock=99999999&page={page}&offset={offset}&sort=desc&apikey={BSCSCAN_API_KEY}"
                )
                if contract_address:
                    url += f"&contractaddress={contract_address}"
                resp = requests.get(url)
                resp.raise_for_status()
                data = resp.json()
                if data.get("status") != "1":
                    return f"❗ Failed to retrieve token transfer history: {data.get('message')}"
                transfers = data.get("result", [])
                summary = []
                for tx in transfers:
                    value = int(tx.get("value", 0)) / (
                        10 ** int(tx.get("tokenDecimal", 18))
                    )
                    summary.append(
                        f"- {tx.get('tokenSymbol', '')} | From: {tx.get('from')[:10]}... → To: {tx.get('to')[:10]}... | Value: {value:.4f}"
                    )
                return f"🔄 Recent BEP-20 transfers:\n" + "\n".join(summary)

            else:
                return "❗ This mode is not supported. ['total_supply', 'source_code', 'normal_tx', 'token_transfers'] 중 하나를 사용하세요."

        except Exception as e:
            return f"❗ Error Running BSCScanTool: {e}"


# ❌ 홀더 수 조회는 BSCScan에서 직접적인 API 미제공
# 참고: 토큰 전송 기록을 통해 추정하거나, 외부 서비스(Covalent 등) 필요
