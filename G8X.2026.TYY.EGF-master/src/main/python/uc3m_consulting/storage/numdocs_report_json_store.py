"""Logic for specific management of the NumdocsReport json file"""

from uc3m_consulting.cfg.enterprise_manager_config import NUMDOCS_STORE_FILE
from .json_store import JsonStore

class NumDocsReportJsonStore():
    """Class for storing the NumdocsReports in json files"""
    #pylint: disable=invalid-name
    class __NumdocsReportJsonStore(JsonStore):
        """Class for dealing NumDocsRecordsJsonStore"""
        def __init__(self, file_name=NUMDOCS_STORE_FILE):
            super().__init__(file_name)

    instance = None

    def __new__(cls, file_name=NUMDOCS_STORE_FILE):
        if cls.instance is None:
            #notice that the singleton creates a single instance with the filename
            #future calls with other file_names won't change it because the instance already exists
            #In case you need to change the file name you must implement a solution
            cls.instance = cls.__NumdocsReportJsonStore(file_name)
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
