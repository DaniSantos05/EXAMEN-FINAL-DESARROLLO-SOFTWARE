"""Module """
from uc3m_consulting.data.enterprise_project import EnterpriseProject
from uc3m_consulting.data.project_document import ProjectDocument
from uc3m_consulting.storage.documents_json_store import DocumentsJsonStore
from uc3m_consulting.storage.projects_json_store import ProjectsJsonStore
from uc3m_consulting.reports.numdocs_report import NumDocsReport
from uc3m_consulting.data.project_budget import ProjectBudget

class EnterpriseManager:
    """Singleton class for the Enterprise Manager"""
    #pylint: disable=invalid-name
    class __EnterpriseManager:
        """Class for providing the methods for managing the orders"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments, too-many-positional-arguments
        def register_project(self,
                             company_cif: str,
                             project_acronym: str,
                             project_description: str,
                             department: str,
                             date: str,
                             budget: str):
            """Saves the Project data into the Projects store"""
            new_project = EnterpriseProject(company_cif=company_cif,
                                            project_acronym=project_acronym,
                                            project_description=project_description,
                                            department=department,
                                            starting_date=date,
                                            project_budget=budget)

            projects_store = ProjectsJsonStore()
            projects_store.add_item(new_project.to_json())
            return new_project.project_id

        def register_document(self, filename: str):
            """saves document data from filename in the Documents store"""
            document = ProjectDocument.get_document_from_file(filename)
            documents_store = DocumentsJsonStore()
            documents_store.add_item(document.to_json())
            return document.document_signature

        def calculate_budget(self, project_id: str):
            """calculate the budget for a given iban"""
            project_budget = ProjectBudget(project_id)
            project_budget.save_budget()
            return True

        def find_docs(self, date_str):
            """
            Generates a JSON report counting valid documents for a specific date.

            Checks cryptographic hashes and timestamps to ensure historical data integrity.
            Saves the output to 'resultado.json'.

            Args:
                date_str (str): date to query.

            Returns:
                number of documents found if report is successfully generated and saved.

            Raises:
                EnterpriseManagementException: On invalid date, file IO errors,
                    missing data, or cryptographic integrity failure.
            """
            report = NumDocsReport(date_str)
            report.save_report()
            return report.num_docs


    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = cls.__EnterpriseManager()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
