import json
from ape import Contract
from eth_utils import from_wei

class ProfitManager:
    def __init__(self, contract_address:str,
                 abi_file:str="CreditGuild/contracts/ProfitManagerABI.json"):
        self.contract = Contract(contract_address, abi=abi_file)
    
    def fetch_total_debt(self):
        """Return the total debt in this CreditGuild contract."""
        debt = self.contract.totalIssuance()
        return from_wei(debt, 'ether')
