import requests

base_url = "https://api.geckoterminal.com/api/v2"

def fetch_prices(network: str, addresses: str):
    url = f"{base_url}/simple/networks/{network}/token_price/{addresses}"

    headers = {
        "Accept": "application/json;version=20230302",
    }
    response = requests.get(url, headers=headers)

    prices = response.json()["data"]["attributes"]["token_prices"]

    any_price = float(next(iter(prices.values())))
    
    return any_price

def fetch_networks():
    url = f"{base_url}/networks"

    headers = {
        "Accept": "application/json;version=20230302",
    }
    response = requests.get(url, headers=headers)
    return response.json()