"""Definition of transfer_type concept"""
from .attribute import Attribute

class Department(Attribute):
    """Definition of attribute department class"""
    # pylint: disable= too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute department init method"""
        super().__init__()
        self._validation_pattern = r"(HR|FINANCE|LEGAL|LOGISTICS)"
        self._error_message = "Invalid department"
        self._attr_value = self._validate(attr_value)
