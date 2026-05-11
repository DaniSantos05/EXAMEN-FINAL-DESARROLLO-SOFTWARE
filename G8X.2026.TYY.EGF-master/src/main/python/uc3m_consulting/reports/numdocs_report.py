"""Class for reporting the number of documents for a given date"""
from datetime import datetime, timezone
from uc3m_consulting.storage.numdocs_report_json_store import NumDocsReportJsonStore
from uc3m_consulting.storage.documents_json_store import DocumentsJsonStore
from uc3m_consulting.data.project_document import ProjectDocument
from uc3m_consulting.exceptions.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.date_attribute import DateAttribute

class NumDocsReport():
    """Class for reporting the number of documents for a given date"""
    def __init__(self, date):
        self.query_date = DateAttribute(date).value
        self.report_date = datetime.now(timezone.utc).timestamp()
        self.num_docs = self.get_num_docs()

    def to_json(self):
        """Convert the report to a json object"""
        return {"Querydate": self.query_date,
                "ReportDate": self.report_date,
                "Numfiles": self.num_docs
                }
    def get_num_docs(self):
        """get the number of documents for a given date"""
        documents_store = DocumentsJsonStore()
        documents_found = documents_store.find_documents_by_date(self.query_date)
        if len(documents_found) == 0:
            raise EnterpriseManagementException("No documents found")
        for document in documents_found:
            ProjectDocument.create_document_from_dict(document)
        return len(documents_found)

    def save_report(self):
        """Save the number of documents for a given date"""
        numdocs_store = NumDocsReportJsonStore()
        numdocs_store.add_item(self.to_json())
