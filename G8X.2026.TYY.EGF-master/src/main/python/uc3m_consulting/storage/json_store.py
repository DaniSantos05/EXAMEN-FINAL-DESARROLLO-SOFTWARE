"""JsonStore definition"""
import json
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException


class JsonStore():
    """JsonStore class"""



    def __init__(self, file_name):
        self._data_list = []
        self._file_name = file_name
        self.load_list_from_file()



    def save_list_to_file( self ):
        """saves the list in the store"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file or file path") from ex

    def load_list_from_file( self ):
        """load the list of items from the store"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
            # append the delivery info

    def add_item( self, item ):
        """add a new item in the store"""
        self.load_list_from_file()
        self._data_list.append(item)
        self.save_list_to_file()

    def find_items( self, item_to_find ):
        """find an item in the store"""
        self.load_list_from_file()
        result = []
        for item in self._data_list:
            if item == item_to_find:
                result.append(item)
        return result

    def find_items_by_key(self, key, value):
        """returns a list with the items that contains the
        pair key:value received """
        self.load_list_from_file()
        result_list = []
        for item in self._data_list:
            if item[key] == value:
                result_list.append(item)
        return result_list
