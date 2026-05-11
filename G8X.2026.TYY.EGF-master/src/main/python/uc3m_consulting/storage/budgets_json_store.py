"""Logic for specific management of the cash flows json file"""

from uc3m_consulting.cfg.enterprise_manager_config import BUDGETS_JSON_STORE
from .json_store import JsonStore

# pylint: disable=too-few-public-methods
class BudgetsJsonStore():
    """Singleton for BudgetsJsonStore"""

    # pylint: disable=invalid-name
    class __BudgetsJsonStore(JsonStore):
        """Class for dealing BudgetsJsonStore"""
        def __init__(self, file_name=BUDGETS_JSON_STORE):
            super().__init__(file_name)

    instance = None

    def __new__(cls, *args, **kwargs):
        # notice that the singleton creates a single instance with the filename
        # future calls with other file_names won't change it because the instance already exists
        # In case you need to change the file name you must implement a solution
        if cls.instance is None:
            cls.instance = cls.__BudgetsJsonStore(*args, **kwargs)
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
