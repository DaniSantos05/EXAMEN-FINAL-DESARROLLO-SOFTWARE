"""Definition of DepositAmmount """
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from .attribute import Attribute

class ProjectBudgetValue(Attribute):
    """Definition of attribute DepositAmount class"""
    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute TransferAmount init method"""
        #not necessary the regex
        super().__init__()
        self._validation_pattern = r"^\d+\.\d{1,2}$"
        self._error_message = "Invalid budget amount"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        attr_value = super()._validate(str(attr_value))
        float_value = float(attr_value)
        if '.' in attr_value:
            decimales = len(attr_value.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if float_value < 50000 or float_value > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")
        return float(float_value)
