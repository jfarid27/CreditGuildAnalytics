import json
from ape import Contract
from eth_utils import from_wei

class SurplusGuildMinter:
    """Interface to a Surplus Guild Minter for a specific credit market."""
    def __init__(self, contract_address:str,
                 abi_file:str="contracts/CreditGuild/SurplusGuildMinterABI.json"):
        self.contract = Contract(contract_address, abi=abi_file)
    
    def fetch_user_stake(self, user_address:str, term_address:str):
        """Return the total stake for the user in the given term for this SGM."""
        stake_details = self.contract.getUserStake(user_address, term_address)
        return from_wei(stake_details['credit'], 'ether')
