import pandas as pd
from time import sleep
from models.CreditGuild.GuildToken import GuildToken
from models.CreditGuild.LoanTerm import LoanTerm

def fetch_terms_and_debt(guild_token_address:str, slow=True, debug=False):
    """
    Fetches the active lending terms and debt information for a given guild token address.
    Parameters:
    - guild_token_address (str): The address of the guild token.
    - slow (bool, optional): Whether to slow down the fetching process to avoid rate limiting. Defaults to True.
    - debug (bool, optional): Whether to enable debugging mode. Defaults to False.
    Returns:
    - pandas.DataFrame: A DataFrame containing the fetched lending terms and debt information.
    """
    
    guild_token = GuildToken(guild_token_address)
    
    count = 0
    totals = []

    terms = guild_token.active_guages()
    for term_address in terms:
        slow and sleep(0.5) # Slow down to avoid rate limiting
        if debug and count > 3:
            # For debugging purposes, only fetch a few terms
            break
        term_contract = LoanTerm(term_address)
        profit_manager_addr = term_contract.get_profit_manager()
        ct = term_contract.get_credit_token()
        colToken = term_contract.get_collateral_token()
        ir = term_contract.get_interest_rate()

        total_issued = term_contract.get_debt()
        totals.append({
            'termAddress': term_address,
            'creditToken': ct,
            'collateral': colToken,
            'interestRate': ir,
            'profitManager': profit_manager_addr,
            'totalIssuance': total_issued
        })
        count += 1

    return pd.DataFrame(totals)