"""Logic for specific management of the Documents json file"""
from datetime import datetime
from uc3m_consulting.cfg.enterprise_manager_config import DOCUMENTS_STORE_FILE
from .json_store import JsonStore

class DocumentsJsonStore():
    """Singleton class for dealing with Documents json files"""
    #pylint: disable=invalid-name
    class __DocumentsJsonStore(JsonStore):
        """Class for dealing DocumentsJsonStore"""
        def __init__(self, file_name=DOCUMENTS_STORE_FILE):
            super().__init__(file_name)

        def find_documents_by_date(self, date):
            """retreive the documents for a given date"""
            self.load_list_from_file()
            documents_found = []
            for document in self._data_list:
                doc_date_str = (datetime.
                                fromtimestamp(document["register_date"]).
                                strftime("%d/%m/%Y"))
                if doc_date_str == date:
                    documents_found.append(document)
            return documents_found
    instance = None

    def __new__(cls, filename=DOCUMENTS_STORE_FILE):
        # notice that the singleton creates a single instance with the filename
        # future calls with other file_names won't change it because the instance already exists
        # In case you need to change the file name you must implement a solution
        if cls.instance is None:
            cls.instance = cls.__DocumentsJsonStore(file_name=filename)
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
