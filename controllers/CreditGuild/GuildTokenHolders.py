from typing import List
import pandas as pd
from time import sleep
from models.CreditGuild.GuildToken import GuildToken

def fetch_holders(addresses:List[str], guild_token_address:str, slow=True, debug=False):
    """
    Fetches the token holders' addresses and balances for a given list of addresses and a guild token address.

    Parameters:
    addresses (List[str]): A list of addresses for which to fetch the token balances.
    guild_token_address (str): The address of the guild token.
    slow (bool, optional): Whether to fetch the balances slowly. Defaults to True.
    debug (bool, optional): Whether to print debug information. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the token holders' addresses and balances.
    """
    token = GuildToken(guild_token_address)
    holders = []
    count = 0
    for address in addresses:
        if debug and count >3:
            break
        if slow:
            sleep(0.1)
        if debug:
            print(f"Fetching balance for {address}")
        bal = token.balance_of(address)
        holders.append({ "address": address, "balance": bal })
        count += 1
    return pd.DataFrame(holders)