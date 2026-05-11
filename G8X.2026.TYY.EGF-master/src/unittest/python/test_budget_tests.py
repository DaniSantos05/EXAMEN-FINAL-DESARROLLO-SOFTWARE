"""Tests for calculate budget"""
#pylint: disable=broad-exception-caught
import datetime
from unittest import TestCase
import os.path
from os import remove
import json
import hashlib
from freezegun import freeze_time
from uc3m_consulting import (BUDGETS_JSON_STORE,
                             EnterpriseManagementException,
                             EnterpriseManager,
                             CASH_FLOWS_JSON_STORE,
                             JSON_FILES_PATH)

NOMBRE_FICHERO_TEMPORAL = JSON_FILES_PATH + "swap.json"
EMPTY_TRANSACTIONS_FILE = JSON_FILES_PATH + "flows_empty_test.json"
NO_JSON_TRANSACTIONS_FILE = JSON_FILES_PATH + "flows_no_json.json"

class TestCalculateBudget(TestCase):
    """Calculate budget tests class"""
    def setUp(self):
        """ inicializo el entorno de prueba """
        if os.path.exists(BUDGETS_JSON_STORE):
            remove(BUDGETS_JSON_STORE)

    @staticmethod
    def read_file():
        """ this method read a Json file and return the value """
        try:
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    @freeze_time("2025/03/26 14:00:00")
    def test_calculate_budget_1 (self):
        """path 1: all ok - entering the loop"""
        mngr = EnterpriseManager()
        res = mngr.calculate_budget(project_id="53474ec11ff2175359b957aeb3ae2f8d")
        self.assertTrue(res)
        data = self.read_file()
        data_found = False
        for budget in data:
            if (budget["PROJECT_ID"] == "53474ec11ff2175359b957aeb3ae2f8d" and
                    budget["timestamp"] ==
                    datetime.datetime.now(datetime.timezone.utc).timestamp() and
                    round(budget["BUDGET"])==round(-4181.36)):
                data_found = True

        self.assertTrue(data_found)

    def test_file_wrong_project_id(self):
        """path with wrong project_id number (exception)"""
        mngr = EnterpriseManager()

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(EnterpriseManagementException) as cm_obj:
            mngr.calculate_budget("ES$559005439021242088295")
        self.assertEqual("Invalid Project ID",cm_obj.exception.message)

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    def test_file_not_found(self):
        """path with transactions file not found"""
        # rename the manipulated order's store
        self.rename_file(CASH_FLOWS_JSON_STORE,NOMBRE_FICHERO_TEMPORAL )
        mngr = EnterpriseManager()
        res = False
        msg = ""
        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""

        try:
            mngr.calculate_budget(project_id="53474ec11ff2175359b957aeb3ae2f8d")
        except EnterpriseManagementException as ex:
            #Error message updated after refactoring JsonStore
            #if ex.message == "Wrong file  or file path":
            if ex.message == "PROJECT_ID not found":
                res = True
            else:
                msg = ex.message
        except Exception as  ex:
            msg = str(ex)

        self.rename_file(NOMBRE_FICHERO_TEMPORAL,CASH_FLOWS_JSON_STORE)
        self.assertEqual(True,res,msg)

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    def test_file_not_json(self):
        """path with transactions file without json format"""
        # rename the transactions file and setting a new empty transactions file
        self.rename_file(CASH_FLOWS_JSON_STORE,NOMBRE_FICHERO_TEMPORAL )
        self.rename_file(NO_JSON_TRANSACTIONS_FILE, CASH_FLOWS_JSON_STORE)
        mngr = EnterpriseManager()
        res = False
        msg = ""
        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        try:
            mngr.calculate_budget(project_id="53474ec11ff2175359b957aeb3ae2f8d")
        except EnterpriseManagementException as ex:
            if ex.message == "JSON Decode Error - Wrong JSON Format":
                res = True
            else:
                msg = ex.message
        except Exception as  ex:
            msg = str(ex)

        #renaming the files to the orignal state
        self.rename_file(CASH_FLOWS_JSON_STORE, NO_JSON_TRANSACTIONS_FILE)
        self.rename_file(NOMBRE_FICHERO_TEMPORAL,CASH_FLOWS_JSON_STORE)
        self.assertEqual(True,res,msg)
        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    def test_file_skip_loop(self):
        """path skipping the loop (empty transactions file)"""
        mngr = EnterpriseManager()

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        self.rename_file(CASH_FLOWS_JSON_STORE,NOMBRE_FICHERO_TEMPORAL )
        self.rename_file(EMPTY_TRANSACTIONS_FILE, CASH_FLOWS_JSON_STORE)
        msg = ""
        res = False
        try:
            mngr.calculate_budget(project_id="53474ec11ff2175359b957aeb3ae2f8d")
        except EnterpriseManagementException as ex:
            if ex.message == "PROJECT_ID not found":
                res = True
            else:
                msg = ex.message
        except Exception as ex:
            msg = str(ex)

        self.rename_file(CASH_FLOWS_JSON_STORE, EMPTY_TRANSACTIONS_FILE)
        self.rename_file(NOMBRE_FICHERO_TEMPORAL, CASH_FLOWS_JSON_STORE)
        self.assertEqual(True, res, msg)

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    def test_file_project_id_not_found(self):
        """path for an project_id not in the file"""
        mngr = EnterpriseManager()

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(EnterpriseManagementException) as cm_obj:
            mngr.calculate_budget(project_id="53C74ec11ff2175359b957aeb3ae2f8d")
        self.assertEqual("PROJECT_ID not found", cm_obj.exception.message)

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    def test_budget_file_not_json(self):
        """path with transactions file not in json format"""
        # rename the transactions file and setting a new empty transactions file
        self.rename_file(BUDGETS_JSON_STORE,NOMBRE_FICHERO_TEMPORAL )
        self.rename_file(NO_JSON_TRANSACTIONS_FILE, BUDGETS_JSON_STORE)
        mngr = EnterpriseManager()
        res = False
        msg = ""
        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        try:
            mngr.calculate_budget(project_id="53474ec11ff2175359b957aeb3ae2f8d")
        except EnterpriseManagementException as ex:
            if ex.message == "JSON Decode Error - Wrong JSON Format":
                res = True
            else:
                msg = ex.message
        except Exception as  ex:
            msg = str(ex)

        if os.path.isfile(BUDGETS_JSON_STORE):
            with open(BUDGETS_JSON_STORE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        #renaming the files to the orignal state
        self.rename_file(BUDGETS_JSON_STORE, NO_JSON_TRANSACTIONS_FILE)
        self.rename_file(NOMBRE_FICHERO_TEMPORAL,BUDGETS_JSON_STORE)
        self.assertEqual(True,res,msg)

        self.assertEqual(hash_new, hash_original)


    def rename_file(self, old_name, new_name):
        """renames a file (if it exists)"""
        if os.path.isfile(old_name):
            os.rename(old_name, new_name)
