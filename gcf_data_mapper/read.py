import csv
import json
import os
from enum import Enum
from typing import Any, Optional, Union

import click


class AllowedFileExtensions(Enum):
    JSON = "json"
    CSV = "csv"


def read_csv(file_path: str) -> list[dict[str, Any]]:
    """
    Reads a csv file and returns a list of dictionaries

    :param file_path str: a file path to the csv file
    :return list: a list of dictionaries, where each line in the csv file is
    mapped to a dictionary
    """
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        fieldnames = csv_reader.fieldnames or []
        data = [{field: line[field] for field in fieldnames} for line in csv_reader]
        return data


def read_json(file_path: str) -> Optional[dict]:
    """
    Reads a json file and returns the json object as a dict

    :param file_path str: A file path to the csv file
    :raises JSONDecodeError: if the file cannot be read
    :return dict: A dictionary of the json data
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise e


def read_data_file(
    file_path: str,
) -> Optional[Union[dict[str, Any], list[dict[str, Any]]]]:
    """
    Simple program that validates a file path for existence, type and size,
    then calls a function to read the csv or json file respectively

    :param file_path str: A file path to the csv/json file
    :raises ValueError: if a non csv or json file type is provided
    :raises FileNotFoundError: if the file does not exist
    :raises ValueError: if the file is empty
    :return Optional[Union[dict[str, Any], list[dict[str, Any]]]]: A dictionary or list of dictionaries
    depending on the file type
    """
    file_extension = os.path.splitext(file_path)[1][1:]
    if file_extension not in [e.value for e in AllowedFileExtensions]:
        raise ValueError("Error reading file: File must be a valid json or csv file")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file or directory: '{file_path}'")
    if os.path.getsize(file_path) == 0:
        raise ValueError("Error reading file: File is empty")
    try:
        if file_extension == AllowedFileExtensions.CSV.value:
            return read_csv(file_path)
        return read_json(file_path)
    except Exception as e:
        click.echo(f"Error reading file: {e}")
        raise e
