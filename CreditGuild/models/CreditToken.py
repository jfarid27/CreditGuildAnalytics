import json
from ape import Contract
from eth_utils import from_wei

class CreditToken:
    def __init__(self, contract_address:str,
                 abi_file:str="CreditGuild/contracts/CreditTokenABI.json"):
        self.contract = Contract(contract_address, abi=abi_file)
    
    def balance_of(self, address:str):
        """Return the balance of the given address."""
        params = [address]
        balance = self.contract.balanceOf(*params)
        return from_wei(balance, 'ether')