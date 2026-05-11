"""Definition of TransferDate concept"""
from datetime import datetime
from datetime import timezone
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from .date_attribute import DateAttribute


class ProjectDate(DateAttribute):
    """Definition of attribute TransferDate class"""
    # pylint: disable=too-few-public-methods
    def _validate( self, attr_value ):
        """calls the superclass validation for checking the regex and validate the
        date accoring the range of allowed years and the python's date definition"""
        attr_value = super()._validate(attr_value)
        date_obj = datetime.strptime(attr_value, "%d/%m/%Y").date()
        if date_obj < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")
        if date_obj.year < 2025 or date_obj.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return attr_value
