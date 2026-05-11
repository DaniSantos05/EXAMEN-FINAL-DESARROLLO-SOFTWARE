"""Definition of attribute concept"""
from .attribute import Attribute

class Description(Attribute):
    """Definition of attribute Description class"""
    # pylint: disable= too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute concept init method"""
        super().__init__()
        self._validation_pattern = r"^.{10,30}$"
        self._error_message = "Invalid description format"
        self._attr_value = self._validate(attr_value)
