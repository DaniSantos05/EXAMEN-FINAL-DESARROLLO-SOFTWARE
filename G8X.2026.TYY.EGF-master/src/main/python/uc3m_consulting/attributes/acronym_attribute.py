"""Definition of attribute concept"""
from .attribute import Attribute

class ProjectAcronym(Attribute):
    """Definition of attribute acronym class"""
    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute acronym init method"""
        self._validation_pattern = r"^[a-zA-Z0-9]{5,10}"
        self._error_message = "Invalid acronym"
        self._attr_value = self._validate(attr_value)
