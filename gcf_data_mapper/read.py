import csv
import json
from typing import Any, Optional, Union

import click


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


def read_json(file_path: str) -> dict:
    """
    Reads a json file, and returns a dict

    :param file_path str: A file path to the csv file
    :return dict: A dictionary of the json data
    """
    with open(file_path, "r") as file:
        return json.load(file)


def read_data_file(
    file_path: str,
) -> Optional[Union[dict[str, Any], list[dict[str, Any]]]]:
    """
    Simple program that reads a data file,
    calls a function to read a csv or json file respectively

    :param file_path str: A file path to the csv/json file
    :raises ValueError: if a non csv or json file type is provided
    :return Optional[Union[dict[str, Any], list[dict[str, Any]]]]: A dictionary or list of dictionaries
    depending on the file type
    """
    file_extension = file_path.lower().split(".")[-1]
    if file_extension not in ["json", "csv"]:
        raise ValueError("Error reading file: File must be a valid json or csv file")
    try:
        if file_extension == "csv":
            return read_csv(file_path)
        else:
            return read_json(file_path)
    except Exception as e:
        click.echo(f"Error reading file: {e}")
