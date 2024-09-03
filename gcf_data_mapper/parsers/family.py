from enum import Enum
from typing import Any, Optional

import click
import pandas as pd


class MetadataProperties(Enum):
    pass


# To consider put these into helper functions ?
def _get_family_doc_status():
    return None


def _get_event_data():
    event_type = ""
    status = _get_family_doc_status()

    return status, event_type


def _get_budget(row, source):
    return next(
        (
            funding["BudgetUSDeq"]
            for funding in row["Funding"]
            if funding["Source"] == source
        ),
        None,
    )  # should this be none or empty string?


def _get_family_metadata(row):
    co_financing_budget = _get_budget(row, "Co-Financing")
    gcf_budget = _get_budget(
        row, "GCF"
    )  # should this be the first value or a sum of the multiple finances where this applies, see line 1387
    implementing_agencies = set(
        [entity.get("Name", "") for entity in row.get("Entities", [])]
    )
    regions = set([country.get("Region", "") for country in row.get("Countries", [])])
    result_areas = set(
        [result.get("Area", "") for result in row.get("ResultAreas", [])]
    )
    result_types = set(
        [result.get("Type", "") for result in row.get("ResultAreas", [])]
    )

    status, event_type = _get_event_data()

    metadata = {
        "Regions": list(regions),
        "ProjectID": row.get("ProjectsID", ""),
        "ApprovedRef": row.get("ApprovedRef", ""),
        "Project value (fund spend)": gcf_budget,
        "Project value (co-financing)": co_financing_budget,
        "Implementing Agencies": list(implementing_agencies),
        "Project URL": row.get("ProjectURL", ""),
        "Theme": row.get("Theme", ""),
        "Result Areas": list(result_areas),
        "Result Types": list(result_types),
        "Sector": row.get("Sector", ""),
        "Status": status,
        "event_types": event_type,
    }

    return metadata


def _map_family_data(row):
    # ToDo Map family data
    data = {}

    data["metadata"] = _get_family_metadata(row)

    return data


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
        mapped_families.append({"metadata": _map_family_data(row)})
        breakpoint()

    return mapped_families
