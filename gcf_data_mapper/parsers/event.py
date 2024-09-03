from collections import namedtuple
from enum import Enum
from typing import Any, Optional

import click
import pandas as pd

from gcf_data_mapper.parsers.helpers import verify_required_fields_present


class EventColumnNames(Enum):
    APPROVED = "ApprovalDate"
    UNDER_IMPLEMENTATION = "StartDate"
    COMPLETED = "DateCompletion"
    APPROVED_REF = "ApprovedRef"
    PROJECTS_ID = "ProjectsID"


class EventTypeNames(Enum):
    APPROVED = "Approved"
    UNDER_IMPLEMENTATION = "Under Implementation"
    COMPLETED = "Completed"


Event = namedtuple("event", ["id", "type", "column_name"])


class Events:
    APPROVED = Event(
        1,
        EventTypeNames.APPROVED.value,
        EventColumnNames.APPROVED.value,
    )
    UNDER_IMPLEMENTATION = Event(
        2,
        EventTypeNames.UNDER_IMPLEMENTATION.value,
        EventColumnNames.UNDER_IMPLEMENTATION.value,
    )
    COMPLETED = Event(
        3,
        EventTypeNames.COMPLETED.value,
        EventColumnNames.COMPLETED.value,
    )


def event(projects_data: pd.DataFrame, debug: bool) -> list[Optional[dict[str, Any]]]:
    """Map the GCF event info to new structure.

    :param pd.DataFrame projects_data: The MCF and GCF project data,
        joined on FP num.
    :param bool debug: Whether debug mode is on.
    :return list[Optional[dict[str, Any]]]: A list of GCF families in
        the 'destination' format described in the GCF Data Mapper Google
        Sheet.
    """
    if debug:
        click.echo("📝 Wrangling GCF event data.")

    required_fields = set(str(e.value) for e in EventColumnNames)
    verify_required_fields_present(projects_data, required_fields)

    gcf_events = []
    for _, row in projects_data.iterrows():
        # Check that the row contains a not NA value for at least one of the required
        # dates.
        has_approved = pd.notna(row.at[Events.APPROVED.column_name])
        has_in_progress = pd.notna(row.at[Events.UNDER_IMPLEMENTATION.column_name])
        has_completed = pd.notna(row.at[Events.COMPLETED.column_name])

        if not any([has_approved, has_in_progress, has_completed]):
            print(has_approved, has_in_progress, has_completed)
            print("No event dates")
            continue

        approved_ref = row.at[EventColumnNames.APPROVED_REF.value]
        projects_id = row.at[EventColumnNames.PROJECTS_ID.value]

        if has_approved:
            gcf_events.append(
                {
                    "import_id": f"GCF.event.{approved_ref}.{projects_id}",
                    "event_title": Events.APPROVED.type,
                    "date": row[Events.APPROVED.column_name],
                    "event_type_value": Events.APPROVED.type,
                }
            )

        if has_in_progress:
            gcf_events.append(
                {
                    "import_id": f"GCF.event.{approved_ref}.{projects_id}",
                    "event_title": Events.UNDER_IMPLEMENTATION.type,
                    "date": row[Events.UNDER_IMPLEMENTATION.column_name],
                    "event_type_value": Events.UNDER_IMPLEMENTATION.type,
                }
            )

        if has_completed:
            gcf_events.append(
                {
                    "import_id": f"GCF.event.{approved_ref}.{projects_id}",
                    "event_title": Events.COMPLETED.type,
                    "date": row[Events.COMPLETED.column_name],
                    "event_type_value": Events.COMPLETED.type,
                }
            )

    return gcf_events
