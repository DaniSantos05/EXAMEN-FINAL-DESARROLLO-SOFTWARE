"""Logic for specific management of the cash flows json file"""

from uc3m_consulting.cfg.enterprise_manager_config import CASH_FLOWS_JSON_STORE
from .json_store import JsonStore

class CashFlowsJsonStore():
    """Singleton class for dealing with cash flows json file"""
    #pylint: disable=invalid-name
    class __CashFlowsJsonStore(JsonStore):
        """Class for dealing CashFlowsJsonStore"""
        def __init__(self, file_name=CASH_FLOWS_JSON_STORE):
            super().__init__(file_name)

    instance = None

    def __new__(cls, *args, **kwargs):
        # notice that the singleton creates a single instance with the filename
        # future calls with other file_names won't change it because the instance already exists
        # In case you need to change the file name you must implement a solution
        if cls.instance is None:
            cls.instance = cls.__CashFlowsJsonStore(*args, **kwargs)
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

