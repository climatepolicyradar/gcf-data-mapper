from typing import Any, Optional, cast

import click
import pandas as pd

from gcf_data_mapper.enums.event import Event, EventColumnNames, Events
from gcf_data_mapper.parsers.helpers import strip_nested, verify_required_fields_present


def append_event(
    gcf_events: list,
    event: Event,
    row: pd.Series,
    approved_ref: str,
    projects_id: str,
    n_value: int,
) -> None:
    """Append an event to the master list that is passed in.

    Remember, because lists are mutable in Python, any changes to the
    list inside a function will be reflected outside of it as a
    reference to the object is passed instead of just the value.

    :param list gcf_events: The list of GCF events.
    :param Event event: The event to append.
    :param pd.Series row: The row of data containing GCF event info.
        Each row corresponds to a GCF 'family'.
    :param str approved_ref: The FP number.
    :param str projects_id: The GCF projects ID.
    :param int n_value: The event number for the given GCF family.
    """
    gcf_events.append(
        {
            "import_id": f"GCF.event.{approved_ref}_{projects_id}.n{n_value:04}",
            "family_import_id": f"GCF.family.{approved_ref}.{projects_id}",
            "event_title": event.type,
            "date": row[event.column_name],
            "event_type_value": event.type,
        }
    )


def check_event_dates(row: pd.Series) -> dict[str, bool]:
    """Check if the row contains valid event date values (not NA).

    :param pd.Series row: The row of data to check.
    :return dict[str, bool]: A dict indicating the presence of each
        event date.
    """
    return {
        Events.APPROVED.name: pd.notna(row.at[Events.APPROVED.column_name]),
        Events.UNDER_IMPLEMENTATION.name: pd.notna(
            row.at[Events.UNDER_IMPLEMENTATION.column_name]
        ),
        Events.COMPLETED.name: pd.notna(row.at[Events.COMPLETED.column_name]),
        Events.UNDER_IMPLEMENTATION_SECONDARY.name: pd.isna(
            row.at[Events.UNDER_IMPLEMENTATION.column_name]
        )
        and pd.notna(row.at[Events.UNDER_IMPLEMENTATION_SECONDARY.column_name]),
    }


def initialise_event_counter(
    event_counter: dict[str, int], family_import_id: str
) -> None:
    """Initialise the event counter for a family_import_id if not present.

    Remember, because dictionaries are mutable in Python, any changes to
    the dictionary inside a function will be reflected outside of it as
    a reference to the object is passed instead of just the value.

    :param dict[str, int] event_counter: The event counter dictionary
        containing each family_import_id as a key and its corresponding
        counter of events.
    :param str family_import_id: The family import ID to initialise an
        event counter for.
    """
    if family_import_id not in event_counter:
        event_counter[family_import_id] = 0


def process_event(
    row: pd.Series,
    gcf_events: list,
    event_counter: dict,
    approved_ref: str,
    projects_id: str,
) -> None:
    """Process a row to append events and update the event counter.

    :param pd.Series row: The row of data to process (corresponds to a
        GCF family).
    :param list gcf_events: The master list of already processed GCF
        events.
    :param dict event_counter: The event counter dictionary.
    :param str approved_ref: The FP number.
    :param str projects_id: The GCF projects ID.
    """
    family_import_id = f"GCF.event.{approved_ref}.{projects_id}"
    initialise_event_counter(event_counter, family_import_id)

    event_dates = check_event_dates(row)
    if not any(event_dates.values()):
        click.echo(f"🛑 No event dates found for {approved_ref} {projects_id}.")
        return

    for event_name, has_event in event_dates.items():
        if has_event:
            event = getattr(Events, event_name.upper())
            append_event(
                gcf_events,
                event,
                row,
                approved_ref,
                projects_id,
                event_counter[family_import_id],
            )
            event_counter[family_import_id] += 1


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
    event_counter = {}

    for _, row in projects_data.iterrows():
        row = cast(pd.Series, row.apply(strip_nested))
        approved_ref = row.at[EventColumnNames.APPROVED_REF.value]
        projects_id = row.at[EventColumnNames.PROJECTS_ID.value]
        process_event(row, gcf_events, event_counter, approved_ref, projects_id)

    return gcf_events
