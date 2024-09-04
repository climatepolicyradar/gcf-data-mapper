from enum import Enum


class RequiredDocumentColumns(Enum):
    SOURCE_URL = "Document page permalink"
    TITLE = "Title"
    TRANSLATED_FILES = "Translated files"
    TRANSLATED_TITLES = "Translated titles"
    TYPE = "Type"
    ID = "ID (Unique ID from our CMS for the document)"


class RequiredFamilyDocumentColumns(Enum):
    APPROVED_REF = "ApprovedRef"
    PROJECTS_ID = "ProjectsID"


class IgnoreDocumentTypes(Enum):
    """Filter the following columns out of the GCF document data.

    TODO: Phase 2 GCF/MCF we will need to parse these document types too
    but for now, we will omit them.
    """

    APPROVED_REF = "Policies, strategies, and guidelines"
    PROJECTS_ID = "Country programme"
