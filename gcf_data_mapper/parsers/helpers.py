import pandas as pd


def verify_required_fields_present(
    data: pd.DataFrame, required_fields: set[str]
) -> bool:
    """Map the GCF event info to new structure.

    :param pd.DataFrame data: The DataFrame to check.
    :param set[str] required_fields: The required DataFrame columns.
    :param bool debug: Whether debug mode is on.
    :raise AttributeError if any of the required fields are missing.
    :return bool: True if the DataFrame contains the required fields.
    """
    cols = set(data.columns)
    diff = set(required_fields).difference(cols)
    if diff == set():
        return True

    raise AttributeError(
        f"Required fields '{str(diff)}' not present in df columns '"
        f"{cols if cols != set() else r'{}'}'"
    )


def check_required_column_value_not_na(row: pd.Series, column_enum) -> bool:
    """Check if the row contains valid document column values (not NA)."""
    return all(pd.notna(row[column.value]) for column in column_enum)
