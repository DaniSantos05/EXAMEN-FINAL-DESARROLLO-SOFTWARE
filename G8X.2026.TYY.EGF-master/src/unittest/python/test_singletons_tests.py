"""Tests for sigletons"""
from unittest import TestCase
from uc3m_consulting import EnterpriseManager
from uc3m_consulting import BudgetsJsonStore
from uc3m_consulting import CashFlowsJsonStore
from uc3m_consulting import DocumentsJsonStore
from uc3m_consulting import NumDocsReportJsonStore
from uc3m_consulting import ProjectsJsonStore

class SingletonTest(TestCase):
    """Class for dealing with singletons"""
    def test_enterprise_manger_singleton(self):
        """Tests the singleton for enterprise manager"""
        enterprise_manager1 = EnterpriseManager()
        enterprise_manager2 = EnterpriseManager()
        enterprise_manager3 = EnterpriseManager()
        self.assertEqual(enterprise_manager1, enterprise_manager2)
        self.assertEqual(enterprise_manager1, enterprise_manager3)
        self.assertEqual(enterprise_manager2, enterprise_manager3)

    def test_budget_singleton(self):
        """Tests the singleton for budget json store"""
        budget_manager1 = BudgetsJsonStore()
        budget_manager2 = BudgetsJsonStore()
        budget_manager3 = BudgetsJsonStore()
        self.assertEqual(budget_manager1, budget_manager2)
        self.assertEqual(budget_manager1, budget_manager3)
        self.assertEqual(budget_manager2, budget_manager3)

    def test_cashflow_singleton(self):
        """Tests the singleton for cashflow json store"""
        cashflow_manager1 = CashFlowsJsonStore()
        cashflow_manager2 = CashFlowsJsonStore()
        cashflow_manager3 = CashFlowsJsonStore()
        self.assertEqual(cashflow_manager1, cashflow_manager2)
        self.assertEqual(cashflow_manager1, cashflow_manager3)
        self.assertEqual(cashflow_manager2, cashflow_manager3)

    def test_document_singleton(self):
        """Tests the singleton for document json store"""
        document_manager1 = DocumentsJsonStore()
        document_manager2 = DocumentsJsonStore()
        document_manager3 = DocumentsJsonStore()
        self.assertEqual(document_manager1, document_manager2)
        self.assertEqual(document_manager1, document_manager3)
        self.assertEqual(document_manager2, document_manager3)

    def test_numdocs_singleton(self):
        """Tests the singleton for numdocs reports json store"""
        numdocs_manager1 = NumDocsReportJsonStore()
        numdocs_manager2 = NumDocsReportJsonStore()
        numdocs_manager3 = NumDocsReportJsonStore()
        self.assertEqual(numdocs_manager1, numdocs_manager2)
        self.assertEqual(numdocs_manager1, numdocs_manager3)
        self.assertEqual(numdocs_manager2, numdocs_manager3)

    def test_projects_singleton(self):
        """Tests the singleton for projects json store"""
        projects_manager1 = ProjectsJsonStore()
        projects_manager2 = ProjectsJsonStore()
        projects_manager3 = ProjectsJsonStore()
        self.assertEqual(projects_manager1, projects_manager2)
        self.assertEqual(projects_manager1, projects_manager3)
        self.assertEqual(projects_manager2, projects_manager3)
