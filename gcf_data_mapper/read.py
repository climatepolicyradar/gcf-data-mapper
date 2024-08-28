import csv
import json
from typing import Any, Optional

import click


def read_csv(file_path: str) -> list[str]:
    """
    Reads a csv file and returns a list of values

    :param str: a file path to the csv file
    :return list: A list of strings
    """
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = []
        for line in csv_reader:
            data.append(line["country"])
        return data


def read_json(file_path: str) -> dict:
    """
    Reads a json file, and returns a dict

    :param str: A file path to the csv file
    :return dict: A dictionary of the json data
    """
    with open(file_path, "r") as file:
        return json.load(file)


def read_data_file(file_path: str) -> Optional[dict[str, Any] | list[str]]:
    """
    Simple program that reads a data file,
    calls a function to read a csv or json file respectively

    :param str: A file path to the csv/json file
    """
    file_extension = file_path.lower().split(".")[-1]
    if file_extension not in ["json", "csv"]:
        raise ValueError("Error reading file: File must be a valid json or csv file")
    try:
        if file_extension == "csv":
            return read_csv(file_path)
        elif file_extension == "json":
            return read_json(file_path)
    except Exception as e:
        click.echo(f"Error reading file: {e}")