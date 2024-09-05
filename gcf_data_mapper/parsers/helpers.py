import pandas as pd


def verify_required_fields_present(
    data: pd.DataFrame, required_fields: set[str]
) -> bool:
    """Map the GCF event info to new structure.

    :param pd.DataFrame data: The DataFrame to check.
    :param set[str] required_fields: The required DataFrame columns.
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


def check_row_for_columns_with_empty_values(
    row: pd.Series, required_columns: list[str]
):
    """
    Check that all required values in the given row are not empty (notna).

    :param pd.Series row: The row to check for notna values.
    :param list[str] required_columns: A list of column names that will be used to verify.
    :raises ValueError: If any value in the row is notna.
    """

    # Ensure we are working with a pandas Series by re-selecting the required columns as a Series
    row_subset = pd.Series(row[required_columns], index=required_columns)

    breakpoint()
    if row_subset.isna().any():
        raise ValueError("This row has empty values")


def check_row_for_missing_columns(row: pd.Series, required_columns: list[str]):
    """
    Check if a given row contains all required columns.

    :param pd.Series row: The row (Series) to check for missing columns.
    :param list[str] required_columns: A list of column names that will be used to verify.
    :raises AttributeError: If any required columns are missing from the row.
    """

    missing_columns = set(required_columns).difference(set(row.index))

    if missing_columns:
        raise AttributeError(
            "The data series is missing these required columns: {}".format(
                ", ".join(missing_columns)
            )
        )
