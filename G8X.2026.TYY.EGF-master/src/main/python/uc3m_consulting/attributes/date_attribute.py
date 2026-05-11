"""Definition of TransferDate concept"""
from datetime import datetime
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from .attribute import Attribute


class DateAttribute(Attribute):
    """Definition of attribute DateAttribute class"""
    # pylint:  disable=too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute Date init method"""
        super().__init__()
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message = "Invalid date format"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        """calls the superclass validation for checking the regex and validate the
        date according the range of allowed years and the python's date definition"""
        attr_value = super()._validate(attr_value)

        try:
            date_obj = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex
        return date_obj.strftime("%d/%m/%Y")
