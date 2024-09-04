import json
from ape import Contract
from eth_utils import from_wei

class LoanTerm:
    def __init__(self, contract_address:str,
                 abi_file:str="contracts/CreditGuild/LoanTermABI.json"):
        self.contract = Contract(contract_address, abi=abi_file)

    def active_guages(self):
        """Return active lending terms in the CreditGuild contract."""
        params = []
        return self.contract.liveGauges(*params)

    def get_credit_token(self):
        """Return the credit token contract address."""
        refs = self.contract.getReferences()
        return refs["creditToken"]
    
    def get_profit_manager(self):
        """Return the profit manager contract address."""
        return self.contract.profitManager()
    
    def get_collateral_token(self):
        """Return the collateral token contract address."""
        params = self.contract.getParameters()
        return params["collateralToken"]
    
    def get_interest_rate(self):
        params = self.contract.getParameters()
        return from_wei(params['interestRate'], 'ether')
    
    def get_debt(self):
        """Return the total debt issued by the loan term."""
        return from_wei(self.contract.issuance(), 'ether')

    