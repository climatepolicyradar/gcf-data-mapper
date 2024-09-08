from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.enums.family import (
    FamilyColumnsNames,
    FamilyNestedColumnNames,
    GCFProjectBudgetSource,
)
from gcf_data_mapper.parsers.helpers import (
    arrays_contain_empty_values,
    check_row_for_missing_columns,
    row_contains_columns_with_empty_values,
)


def get_budgets(funding_list: list[dict], source: str) -> list[int]:
    """Get the budget amount from the row based on the funding source.

    :param list[dict] row: A list of all the funding information, represented in dictionaries
    :param str source: The funding source to retrieve the budget from.

    :return list[int]: A list of budget amounts corresponding to the source,
        or [0] if the source is not found.
    """

    budget_key = FamilyNestedColumnNames.BUDGET.value
    source_key = FamilyNestedColumnNames.SOURCE.value

    budgets = [
        funding[budget_key] for funding in funding_list if funding[source_key] == source
    ]

    return budgets if budgets else [0]


def map_family_metadata(row: pd.Series) -> Optional[dict]:
    """Map the metadata of a family based on the provided row.

    :param pd.Series row: The row containing family information.
    :return dict: A dictionary containing mapped metadata for the family.
    """

    countries = row.at[FamilyColumnsNames.COUNTRIES.value]
    entities = row.at[FamilyColumnsNames.ENTITIES.value]
    funding_sources = row.at[FamilyColumnsNames.FUNDING.value]
    result_areas = row.at[FamilyColumnsNames.RESULT_AREAS.value]

    area_key = FamilyNestedColumnNames.AREA.value
    name_key = FamilyNestedColumnNames.NAME.value
    region_key = FamilyNestedColumnNames.REGION.value
    type_key = FamilyNestedColumnNames.TYPE.value

    co_financing_budgets = get_budgets(
        funding_sources, GCFProjectBudgetSource.CO_FINANCING.value
    )
    gcf_budgets = get_budgets(funding_sources, GCFProjectBudgetSource.GCF.value)

    implementing_agencies = [entity[name_key] for entity in entities]
    regions = [country[region_key] for country in countries]
    areas = [result[area_key] for result in result_areas]
    types = [result[type_key] for result in result_areas]

    # As we are filtering the budget information by source for gcf and co financing, we
    # know there will be instances where only one type of funding exists so checking
    # for empty/false values would create false positives, hence the exclusion from this
    # check
    if arrays_contain_empty_values(
        [
            ("Implementing Agencies", implementing_agencies),
            ("Regions", regions),
            ("Result Areas", areas),
            ("Result Types", types),
        ],
        row.at[FamilyColumnsNames.PROJECTS_ID.value],
    ):
        return None

    metadata = {
        "approved_ref": [row.at[FamilyColumnsNames.APPROVED_REF.value]],
        "implementing_agencies": list(set(implementing_agencies)),
        "project_id": [row.at[FamilyColumnsNames.PROJECTS_ID.value]],
        "project_url": [row.at[FamilyColumnsNames.PROJECT_URL.value]],
        "project_value_fund_spend": gcf_budgets,
        "project_value_co_financing": co_financing_budgets,
        "regions": list(set(regions)),
        "result_areas": list(set(areas)),
        "result_types": list(set(types)),
        "sector": [row.at[FamilyColumnsNames.SECTOR.value]],
        "theme": [row.at[FamilyColumnsNames.THEME.value]],
    }

    return metadata


def process_row(row: pd.Series) -> Optional[dict]:
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
        click.echo(
            f"🛑 Skipping row as it contains empty column values: See Project {doc_id}"
        )
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
        mapped_families.append(process_row(row))

    return mapped_families
