"""Deposit into account test cases """
import csv
import json
import os.path
import hashlib
from unittest import TestCase
from os import remove
from freezegun import freeze_time
from uc3m_consulting import (JSON_FILES_PATH,
                        DOCUMENTS_STORE_FILE,
                        EnterpriseManager,
                        JSON_INPUT_FILES_RF2,
                        EnterpriseManagementException)

class TestRegisterDocumentTests(TestCase):
    """Test class for deposit method"""
    def setUp(self):
        """ inicializo el entorno de prueba """
        if os.path.exists(DOCUMENTS_STORE_FILE):
            remove(DOCUMENTS_STORE_FILE)

    def tearDown(self):
        """ dejo limpio el entorno de prueba """
        if os.path.exists(DOCUMENTS_STORE_FILE):
            remove(DOCUMENTS_STORE_FILE)

    @staticmethod
    def read_file():
        """ this method read a Json file and return the value """
        try:
            with open(DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    @freeze_time("2025/03/26 14:00:00")
    #pylint: disable=too-many-locals
    def test_parametrized_cases(self):
        """Parametrized cases read from testingCases_RF2.csv
        time is set to 01/07/2024 since it is the chosen for the valid case"""
        my_cases = JSON_FILES_PATH + "test_cases_2026_method2.csv"
        with open(my_cases, newline='', encoding='utf-8') as csvfile:
            param_test_cases = csv.DictReader(csvfile, delimiter=',')
            mngr = EnterpriseManager()
            for row in param_test_cases:
                # VALID INVALID;ID TEST;FILE;EXPECTED RESULT
                test_id = row['ID_TEST']
                valid = row["VALID_INVALID"]
                result = row["RESULT"]
                test_file = JSON_INPUT_FILES_RF2 + row["FILE"]
                if valid == "VALID":
                    with self.subTest(test_id + valid):
                        # removes all the deposits to be sure that the method works
                        self.setUp()
                        valor = mngr.register_document(test_file)
                        self.assertEqual(result, valor)
                        # Check if this deposit has been stored

                        my_data = self.read_file()
                        found = False
                        for k in my_data:
                            if k["document_signature"] == valor:
                                found = True
                        # if found is False , this assert fails
                        self.assertTrue(found)
                else:
                    with self.subTest(test_id + valid):
                        # read the file to compare file content before and after method call
                        if os.path.isfile(DOCUMENTS_STORE_FILE):
                            with open(DOCUMENTS_STORE_FILE, "r",
                                      encoding="utf-8", newline="") as file_org:
                                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
                        else:
                            hash_original = ""

                        with self.assertRaises(EnterpriseManagementException) as c_m:
                            valor = mngr.register_document(test_file)
                        self.assertEqual(c_m.exception.message, result)
                        if os.path.isfile(DOCUMENTS_STORE_FILE):
                            with open(DOCUMENTS_STORE_FILE, "r",
                                      encoding="utf-8", newline="") as file:
                                hash_new = hashlib.md5(str(file).encode()).hexdigest()
                        else:
                            hash_new = ""
                        self.assertEqual(hash_new, hash_original)
