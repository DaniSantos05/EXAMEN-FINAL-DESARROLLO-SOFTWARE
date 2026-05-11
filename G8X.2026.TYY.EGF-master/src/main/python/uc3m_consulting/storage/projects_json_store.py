"""Logic for specific management of the Transfer json file"""

from uc3m_consulting.cfg.enterprise_manager_config import PROJECTS_STORE_FILE
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from .json_store import JsonStore

class ProjectsJsonStore():
    """Singleton class for dealing with ProjectsJsonStore"""
    #pylint: disable=invalid-name
    class __ProjectsJsonStore(JsonStore):
        """Class for dealing TransfersJsonStore"""
        def __init__(self, file_name=PROJECTS_STORE_FILE):
            super().__init__(file_name)

        def add_item(self, item):
            """Overrides the original method including the logic"""
            self.load_list_from_file()
            if self.find_items(item_to_find=item):
                raise EnterpriseManagementException("Duplicated project in projects list")
            super().add_item(item)

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__ProjectsJsonStore(*args, **kwargs)
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
