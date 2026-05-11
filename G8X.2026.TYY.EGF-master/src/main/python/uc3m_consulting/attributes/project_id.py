"""Attribute for validating Project ID"""
from .attribute import Attribute

class ProjectID(Attribute):
    """Attribute for validating Project ID"""
    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^[a-fA-F0-9]{32}$"
        self._error_message = "Invalid Project ID"
        self._attr_value = self._validate(attr_value)
