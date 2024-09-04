from collections import namedtuple
from enum import Enum

Event = namedtuple("event", ["name", "type", "column_name"])


class RequiredEventColumns(Enum):
    """The fields the GCF data mapper needs to parse event data."""

    APPROVED = "ApprovalDate"
    UNDER_IMPLEMENTATION = "StartDate"
    COMPLETED = "DateCompletion"
    APPROVED_REF = "ApprovedRef"
    PROJECTS_ID = "ProjectsID"


class EventTypeNames(Enum):
    """The GCF event type names (should map to the GCF taxonomy)."""

    APPROVED = "Approved"
    UNDER_IMPLEMENTATION = "Under Implementation"
    COMPLETED = "Completed"


class Events:
    APPROVED = Event(
        "approved",
        EventTypeNames.APPROVED.value,
        RequiredEventColumns.APPROVED.value,
    )
    UNDER_IMPLEMENTATION = Event(
        "under_implementation",
        EventTypeNames.UNDER_IMPLEMENTATION.value,
        RequiredEventColumns.UNDER_IMPLEMENTATION.value,
    )
    COMPLETED = Event(
        "completed",
        EventTypeNames.COMPLETED.value,
        RequiredEventColumns.COMPLETED.value,
    )
