"""Contains the class OrderShipping"""
from datetime import datetime, timezone
import hashlib
import json
from freezegun import freeze_time
from uc3m_consulting.attributes.project_id import ProjectID
from uc3m_consulting.attributes.file_name import FileName
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException


class ProjectDocument():
    """Class representing the information required for shipping of an order"""

    def __init__(self, project_id: str, file_name):
        self.__alg = "SHA-256"
        self.__type = "PDF"
        self.__project_id = ProjectID(project_id).value
        self.__file_name = FileName(file_name).value
        justnow = datetime.now(timezone.utc)
        self.__register_date = datetime.timestamp(justnow)

    @classmethod
    def create_document_from_dict(cls, el):
        """Class method that returns a new instance from a dictionary"""
        d_obj = datetime.fromtimestamp(el["register_date"], tz=timezone.utc)
        with freeze_time(d_obj):
            # check the project id (thanks to freezetime)
            # if project_id are different then the data has been
            # manipulated
            p = cls(el["project_id"], el["file_name"])
            if p.document_signature != el["document_signature"]:
                raise EnterpriseManagementException("Inconsistent document signature")
        return p
    @classmethod
    def get_document_from_file(cls, input_file:str):
        """class method that returns a new instance of account deposit
        from the content of the input_file received as a parameter"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                input_data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

        # comprobar valores del fichero
        try:
            project_id = input_data["PROJECT_ID"]
            file_name = input_data["FILENAME"]
        except KeyError as e:
            raise EnterpriseManagementException("Error - Invalid Key in JSON") from e
        new_document = cls(project_id=project_id, file_name=file_name)
        return new_document

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "project_id": self.__project_id,
                "file_name": self.__file_name,
                "register_date": self.__register_date,
                "document_signature": self.document_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",project_id:" + \
               str(self.__project_id) + ",file_name:" + str(self.__file_name) + \
               ",register_date:" + str(self.__register_date) + "}"

    @property
    def project_id(self):
        """Property that represents the product_id of the patient"""
        return self.__project_id

    @project_id.setter
    def project_id(self, value):
        self.__project_id = value

    @property
    def file_name(self):
        """Property that represents the order_id"""
        return self.__file_name
    @file_name.setter
    def file_name(self, value):
        self.__file_name = value

    @property
    def register_date(self):
        """Property that represents the phone number of the client"""
        return self.__register_date
    @register_date.setter
    def register_date(self, value):
        self.__register_date = value


    @property
    def document_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()
