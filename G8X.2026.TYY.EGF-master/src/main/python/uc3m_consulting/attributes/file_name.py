"""Attribute for validating File Name"""
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class FileName(Attribute):
    """Attribute for validating File Name
    <NAME><EXTENSION> where
    <NAME>: 8 CHARACTERS a-z A-Z 0-9
    <EXTESION> .pdf or .docx or .xlsx"""
    def __init__(self, value):
        """Definition of attribute FileName init method"""
        super().__init__()
        self._validation_pattern = r"^[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)$"
        self._error_message = "Invalid File Name"
        self._attr_value = self._validate(value)
