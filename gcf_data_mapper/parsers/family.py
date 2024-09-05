from enum import Enum
from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.parsers.helpers import (
    check_row_for_columns_with_empty_values,
    check_row_for_missing_columns,
)


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


class FamilyNestedColumnNames(Enum):
    """The fields the GCF data mapper needs to parse nested family data/ metadata."""

    AREA = "Area"
    BUDGET = "BudgetUSDeq"
    NAME = "Name"
    REGION = "Region"
    SOURCE = "Source"
    TYPE = "Type"


class GCFProjectBudgetSource(Enum):
    """The source of financing for the project's budget funding"""

    CO_FINANCING = "Co-Financing"
    GCF = "GCF"


# This checks that a key value pair exists on a nested dictionary, we want to be strict
# with our validation so want to be alerted when data that we expect to be there does
# not exist, we can then take this back to the client and handle it accordingly
def _get_value_in_nested_object(object: dict, key: str) -> Any:
    """
    Retrieve the value associated with a given key in a nested dictionary object.

    :param dict object: The dictionary from which to retrieve the value.
    :param str key: The key value that will be used to retrieve that value.

    :raises KeyError: If the specified key does not exist in the dictionary.
    :raises ValueError: If the key exists but the associated value is empty (None,
    empty string, or empty list).

    :return Any: The value associated with the specified key.
    """

    # The get function, checks for a key in a dict and defaults to None instead of
    # raising a key error. However for null values in a json object this converts to a NoneType,
    # so to avoid false positives, we set the default to a specified string so that we
    # can know for sure when a value is empty vs when a key does not exists
    value = object.get(key, "key does not exist")

    if value == "key does not exist":
        raise KeyError(f"key: {key} does not exist on this dict")

    # Check for false values like empty string, empty list, or empty dict or None
    if not value:
        raise ValueError(f"Key '{key}' exists, but the value is empty")

    return value


def _get_budgets(row: pd.Series, source: str) -> list[int]:
    """
    Get the budget amount from the row based on the funding source.

    :param pd.Series row: The row containing funding information.
    :param str source: The funding source to retrieve the budget from.

    :return list[int]: A list of budget amounts corresponding to the source,
    or [0] if the source is not found.
    """

    budgets = [
        _get_value_in_nested_object(funding, FamilyNestedColumnNames.BUDGET.value)
        for funding in row.at[FamilyColumnsNames.FUNDING.value]
        if _get_value_in_nested_object(funding, FamilyNestedColumnNames.SOURCE.value)
        == source
    ]

    return budgets if budgets else [0]


def _map_family_metadata(row: pd.Series) -> dict:
    """
    Map the metadata of a family based on the provided row.

    :param pd.Series row: The row containing family information.
    :return dict: A dictionary containing mapped metadata for the family.
    """

    co_financing_budgets = _get_budgets(row, GCFProjectBudgetSource.CO_FINANCING.value)
    gcf_budgets = _get_budgets(row, GCFProjectBudgetSource.GCF.value)
    implementing_agencies = set(
        [
            _get_value_in_nested_object(entity, FamilyNestedColumnNames.NAME.value)
            for entity in row.at[FamilyColumnsNames.ENTITIES.value]
        ]
    )
    regions = set(
        [
            _get_value_in_nested_object(country, FamilyNestedColumnNames.REGION.value)
            for country in row.at[FamilyColumnsNames.COUNTRIES.value]
        ]
    )
    result_areas = set(
        [
            _get_value_in_nested_object(result, FamilyNestedColumnNames.AREA.value)
            for result in row.at[FamilyColumnsNames.RESULT_AREAS.value]
        ]
    )
    result_types = set(
        [
            _get_value_in_nested_object(result, FamilyNestedColumnNames.TYPE.value)
            for result in row.at[FamilyColumnsNames.RESULT_AREAS.value]
        ]
    )

    metadata = {
        "regions": list(regions),
        "project_id": [row.at[FamilyColumnsNames.PROJECTS_ID.value]],
        "approved_ref": [row.at[FamilyColumnsNames.APPROVED_REF.value]],
        "project_value_fund_spend": gcf_budgets,
        "project_value_co_financing": co_financing_budgets,
        "implementing_agencies": list(implementing_agencies),
        "project_url": [row.at[FamilyColumnsNames.PROJECT_URL.value]],
        "theme": [row.at[FamilyColumnsNames.THEME.value]],
        "result_areas": list(result_areas),
        "result_types": list(result_types),
        "sector": [row.at[FamilyColumnsNames.SECTOR.value]],
    }

    return metadata


def _map_family_data(row: pd.Series) -> dict:
    """
    Map the family data based on the provided row.

    :param pd.Series row: The row containing family information.
    :return dict: A dictionary containing mapped data for the family entity.
    """

    # ToDo Map family data
    return {
        "metadata": _map_family_metadata(row),
    }


def family(projects_data: pd.DataFrame, debug: bool) -> list[Optional[dict[str, Any]]]:
    """Map the GCF family info to new structure.

    :param pd.DataFrame projects_data: The MCF and GCF project data,
        joined on FP num.
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """

    if debug:
        click.echo("📝 Wrangling GCF family data.")

    required_columns = [column.value for column in FamilyColumnsNames]
    mapped_families = []

    for _, row in projects_data.iterrows():
        check_row_for_missing_columns(row, required_columns)
        check_row_for_columns_with_empty_values(row, required_columns)
        mapped_families.append(_map_family_data(row))

    return mapped_families
