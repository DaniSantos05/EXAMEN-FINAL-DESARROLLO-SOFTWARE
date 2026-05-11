"""Class for dealing with iban's balances"""
from datetime import datetime
from datetime import timezone


from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.project_id import ProjectID
from uc3m_consulting.storage.cash_flow_json_store import CashFlowsJsonStore
from uc3m_consulting.storage.budgets_json_store import BudgetsJsonStore

class ProjectBudget():
    """Class that represents the current balance for an PROJECT_ID"""
    def __init__(self, project_id):
        self._project_id = ProjectID(project_id).value
        self._last_budget_time = datetime.timestamp(datetime.now(timezone.utc))
        self._budget = self.calculate_project_budget()

    def calculate_project_budget(self):
        """calculates the current balance for the object's iban code"""
        transactions_storage = CashFlowsJsonStore()

        transactions_list = transactions_storage.find_items_by_key(key="PROJECT_ID",
                                                                   value=self._project_id)
        if len(transactions_list) == 0:
            raise EnterpriseManagementException("PROJECT_ID not found")
        current_balance = 0
        for transaction in transactions_list:
            if "inflow" in transaction.keys():
                current_balance += float(transaction["inflow"])
            else:
                current_balance -= float(transaction["outflow"])
        return current_balance

    def to_json(self):
        """returns the object info in json format"""
        return {"PROJECT_ID": self._project_id,
                "timestamp": self._last_budget_time,
                "BUDGET": self._budget}

    def save_budget(self):
        """saves the current balance of the iban into a json store"""
        balances_storage = BudgetsJsonStore()
        balances_storage.add_item(self.to_json())
