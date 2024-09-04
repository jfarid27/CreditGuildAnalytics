import json
from ape import Contract
from eth_utils import from_wei

class GuildToken:
    def __init__(self, contract_address:str,
                 abi_file:str="CreditGuild/contracts/GuildTokenABI.json"):
        self.contract = Contract(contract_address, abi=abi_file)

    def active_guages(self):
        """Return active lending terms in the CreditGuild contract."""
        params = []
        terms = self.contract.liveGauges(*params)
        return terms
    
    def balance_of(self, address:str):
        """Return the balance of the given address."""
        params = [address]
        balance = self.contract.balanceOf(*params)
        return from_wei(balance, 'ether')