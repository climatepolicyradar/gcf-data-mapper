from enum import Enum


class FamilyColumnsNames(Enum):
    """The fields the GCF data mapper needs to parse family data/ metadata."""

    APPROVED_REF = "ApprovedRef"
    COUNTRIES = "Countries"
    ENTITIES = "Entities"
    FUNDING = "Funding"
    PROJECT_URL = "ProjectURL"
    PROJECTS_ID = "ProjectsID"
    RESULT_AREAS = "ResultAreas"
    SECTOR = "Sector"
    THEME = "Theme"
    TITLE = "ProjectName"
    SUMMARY = "Summary"
    STATUS = "Status"


class FamilyNestedColumnNames(Enum):
    """The fields the GCF data mapper needs to parse nested family data/ metadata."""

    COUNTRY_ISO3 = "ISO3"
    AREA = "Area"
    BUDGET = "BudgetUSDeq"
    NAME = "Name"
    REGION = "Region"
    SOURCE = "Source"
    TYPE = "Type"
    VALUE = "Value"


class GCFProjectBudgetSource(Enum):
    """The source of financing for the project's budget funding"""

    CO_FINANCING = "Co-Financing"
    GCF = "GCF"
