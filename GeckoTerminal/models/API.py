import time
import requests

base_url = "https://api.geckoterminal.com/api/v2"

def fetch_prices(network: str, addresses: str, slow=True):
    url = f"{base_url}/simple/networks/{network}/token_price/{addresses}"

    headers = {
        "Accept": "application/json;version=20230302",
    }

    if slow:
        time.sleep(0.5)
    response = requests.get(url, headers=headers)

    prices = response.json()["data"]["attributes"]["token_prices"]

    if not prices == {}:
        return float(next(iter(prices.values())))

def fetch_networks():
    url = f"{base_url}/networks"

    headers = {
        "Accept": "application/json;version=20230302",
    }
    response = requests.get(url, headers=headers)
    return response.json()