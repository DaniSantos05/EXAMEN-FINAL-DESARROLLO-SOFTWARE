"""Global constants for finding the path"""
import os.path
JSON_FILES_PATH = os.path.join(os.path.dirname(__file__), "../../../../unittest/json_files/")
PROJECTS_STORE_FILE = JSON_FILES_PATH + "projects_store.json"
DOCUMENTS_STORE_FILE = JSON_FILES_PATH + "documents_store.json"
CASH_FLOWS_JSON_STORE = JSON_FILES_PATH + "flows.json"
TRANSACTIONS_STORE_FILE = JSON_FILES_PATH + "transactions.json"
BUDGETS_JSON_STORE = JSON_FILES_PATH + "budgets.json"
BALANCES_STORE_FILE = JSON_FILES_PATH + "balances.json"
NUMDOCS_STORE_FILE = JSON_FILES_PATH + "numdocs_store.json"
#CONSTANTS FOR TESTING FILES WITH DATA FOR
# PROJECTS AND DOCUMENTS ONLY FOR TESTING
TEST_DOCUMENTS_STORE_FILE = JSON_FILES_PATH + "test_documents_store.json"
TEST_PROJECTS_STORE_FILE = JSON_FILES_PATH + "test_projects_store.json"
JSON_INPUT_FILES_RF2 = JSON_FILES_PATH + "/method2_inputs/"
