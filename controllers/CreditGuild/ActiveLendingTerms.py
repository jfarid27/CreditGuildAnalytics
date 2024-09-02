import pandas as pd
from time import sleep
from models.CreditGuild.GuildToken import GuildToken
from models.CreditGuild.LoanTerm import LoanTerm
from models.CreditGuild.SurplusGuildMinter import SurplusGuildMinter

def fetch_user_stakes(user_address:str, terms_df:pd.DataFrame, debug=False, slow=True):
    """
    Fetches the user stakes for a given user address from the provided terms DataFrame.

    Parameters:
    - user_address (str): The address of the user.
    - terms_df (pd.DataFrame): The DataFrame containing the lending terms.
    - debug (bool, optional): If True, enables debug mode and prints debug information. Default is False.
    - slow (bool, optional): If True, enables slow mode and adds a delay of 0.5 seconds between each iteration. Default is True.

    Returns:
    - pd.DataFrame: The DataFrame containing the user stakes for the given user address.
    """
    terms = terms_df[["termAddress", "creditToken", "surplusGuildMinter"]].copy()
    user_stakes = []
    count = 0
    for term in terms.itertuples():
        slow and sleep(0.5)
        if debug and count > 3:
            # For debugging purposes, only fetch a few terms
            break
        sgm = SurplusGuildMinter(term.surplusGuildMinter)
        stake = sgm.fetch_user_stake(user_address, term.termAddress)
        debug and print(f"User stake for {user_address} in {term.termAddress}: {stake}")
        if stake > 0:
            user_stakes.append({"termAddress": term.termAddress, 'userStake': stake})
        count += 1
    if not user_stakes:
        return pd.DataFrame()
    return pd.merge(terms, pd.DataFrame(user_stakes), on="termAddress", how="right")

def fetch_users_stakes(users_df: pd.DataFrame, merged_staking: pd.DataFrame, slow: bool = True):
    """
    Fetches the stakes of multiple users.

    Args:
        users_df (pd.DataFrame): DataFrame containing user information.
        merged_staking (pd.DataFrame): DataFrame containing merged staking data.
        slow (bool, optional): Flag indicating whether to use slow fetching. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame containing the stakes of the users.
    """
    users_stakes = pd.DataFrame()
    for user in users_df.itertuples():
        user_stakes = fetch_user_stakes(user.address, merged_staking, slow=True)
        if not user_stakes.empty:
            user_stakes["address"] = user.address
            users_stakes = pd.concat([users_stakes, user_stakes], ignore_index=True)

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