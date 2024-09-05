from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.enums.family import (
    FamilyColumnsNames,
    FamilyNestedColumnNames,
    GCFProjectBudgetSource,
)
from gcf_data_mapper.parsers.helpers import (
    check_row_for_missing_columns,
    get_value_from_nested_object,
    row_contains_columns_with_empty_values,
)


def get_budgets(row: pd.Series, source: str) -> list[int]:
    """Get the budget amount from the row based on the funding source.

    :param pd.Series row: The row containing funding information.
    :param str source: The funding source to retrieve the budget from.

    :return list[int]: A list of budget amounts corresponding to the source,
    or [0] if the source is not found.
    """

    funding_list = row.at[FamilyColumnsNames.FUNDING.value]

    budgets = [
        get_value_from_nested_object(funding, FamilyNestedColumnNames.BUDGET.value)
        for funding in funding_list
        if get_value_from_nested_object(funding, FamilyNestedColumnNames.SOURCE.value)
        == source
    ]

    return budgets if budgets else [0]


def map_family_metadata(row: pd.Series) -> dict:
    """Map the metadata of a family based on the provided row.

    :param pd.Series row: The row containing family information.
    :return dict: A dictionary containing mapped metadata for the family.
    """

    co_financing_budgets = get_budgets(row, GCFProjectBudgetSource.CO_FINANCING.value)
    gcf_budgets = get_budgets(row, GCFProjectBudgetSource.GCF.value)
    implementing_agencies = set(
        [
            get_value_from_nested_object(entity, FamilyNestedColumnNames.NAME.value)
            for entity in row.at[FamilyColumnsNames.ENTITIES.value]
        ]
    )
    regions = set(
        [
            get_value_from_nested_object(country, FamilyNestedColumnNames.REGION.value)
            for country in row.at[FamilyColumnsNames.COUNTRIES.value]
        ]
    )
    result_areas = set(
        [
            get_value_from_nested_object(result, FamilyNestedColumnNames.AREA.value)
            for result in row.at[FamilyColumnsNames.RESULT_AREAS.value]
        ]
    )
    result_types = set(
        [
            get_value_from_nested_object(result, FamilyNestedColumnNames.TYPE.value)
            for result in row.at[FamilyColumnsNames.RESULT_AREAS.value]
        ]
    )

    metadata = {
        "approved_ref": [row.at[FamilyColumnsNames.APPROVED_REF.value]],
        "implementing_agencies": list(implementing_agencies),
        "project_id": [row.at[FamilyColumnsNames.PROJECTS_ID.value]],
        "project_url": [row.at[FamilyColumnsNames.PROJECT_URL.value]],
        "project_value_fund_spend": gcf_budgets,
        "project_value_co_financing": co_financing_budgets,
        "regions": list(regions),
        "result_areas": list(result_areas),
        "result_types": list(result_types),
        "sector": [row.at[FamilyColumnsNames.SECTOR.value]],
        "theme": [row.at[FamilyColumnsNames.THEME.value]],
    }

    return metadata


def map_family_data(row: pd.Series) -> Optional[dict]:
    """Map the family data based on the provided row.

    :param pd.Series row: The row containing family information.
    :return Optional[dict]: A dictionary containing mapped data for the family entity.
    The function will return None, if the row contains missing data from expected columns/fields
    """

    required_columns = [column.value for column in FamilyColumnsNames]

    doc_id = (
        row.at[FamilyColumnsNames.PROJECTS_ID.value]
        if FamilyColumnsNames.PROJECTS_ID.value in row.index
        and pd.notna(row.at[FamilyColumnsNames.PROJECTS_ID.value])
        else None
    )

    if not doc_id:
        click.echo("🛑 Skipping row as it does not contain a project id")
        return None

    # Check for missing required columns in the row and raise error accordingly
    check_row_for_missing_columns(row, required_columns, doc_id)

    if row_contains_columns_with_empty_values(row, required_columns):
        click.echo(f"🛑 Skipping row as it contains empty column values: See {doc_id}")
        return None

    # ToDo Map family data
    return {
        "metadata": map_family_metadata(row),
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

    mapped_families = []

    for _, row in projects_data.iterrows():
        mapped_families.append(map_family_data(row))

    return mapped_families
