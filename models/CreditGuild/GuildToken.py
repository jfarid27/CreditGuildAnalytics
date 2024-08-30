import json
from ape import Contract

class GuildToken:
    def __init__(self, contract_address:str,
                 abi_file:str="contracts/CreditGuild/GuildTokenABI.json"):
        self.contract = Contract(contract_address, abi=abi_file)

    def active_guages(self):
        """Return active lending terms in the CreditGuild contract."""
        params = []
        terms = self.contract.liveGauges(*params)
        return terms