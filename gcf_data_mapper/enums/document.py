from enum import Enum


class RequiredDocumentColumns(Enum):
    TITLE = "Title"
    TYPE = "Type"
    ID = "ID (Unique ID from our CMS for the document)"
    SOURCE_URL = "Main file (English)"


class TranslatedDocumentColumns(Enum):
    TRANSLATED_FILES = "Translated files"
    TRANSLATED_TITLES = "Translated titles"


class RequiredFamilyDocumentColumns(Enum):
    APPROVED_REF = "ApprovedRef"
    PROJECTS_ID = "ProjectsID"


class IgnoreDocumentTypes(Enum):
    """Filter the following columns out of the GCF document data.

    TODO: Phase 2 GCF/MCF we will need to parse these document types too
    but for now, we will omit them.
    """

    POLICIES_STRATEGIES_GUIDELINES = "Policies, strategies, and guidelines"
    COUNTRY_PROGRAMME = "Country programme"


class DocumentVariantNames(Enum):
    ORIGINAL = "Original Language"
    TRANSLATION = "Translation"
