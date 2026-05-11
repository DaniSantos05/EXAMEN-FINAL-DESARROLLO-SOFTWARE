"""Definition of DepositAmmount """
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from .attribute import Attribute

class ProjectCIF(Attribute):
    """Definition of attribute ProjectCIF class"""
    # pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute TransferAmount init method"""
        #not necessary the regex
        super().__init__()
        self._validation_pattern = r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
        self._error_message = "Invalid CIF format"
        self._attr_value = self._validate(attr_value)

    def _validate( self, attr_value ):
        attr_value = super()._validate(attr_value)
        l = attr_value[0]
        n = attr_value[1:8]
        u = attr_value[8]

        s1 = 0
        s2 = 0

        for i,n_val in enumerate(n):
            if i % 2 == 0:
                x = int(n_val) * 2
                if x > 9:
                    s1 = s1 + (x // 10) + (x % 10)
                else:
                    s1 = s1 + x
            else:
                s2 = s2 + int(n_val)

        t = s1 + s2
        u2 = t % 10
        r = 10 - u2

        if r == 10:
            r = 0

        dic = "JABCDEFGHI"

        if l in ('A', 'B', 'E', 'H'):
            if str(r) != u:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif l in ('P', 'Q', 'S', 'K'):
            if dic[r] != u:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return attr_value
