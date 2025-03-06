"""
Functions for extracting data from CSV and JSON files.
"""
import re
import json
import polars as pl
import logging

logger = logging.getLogger(__name__)


def extract_csv(file_path: str) -> pl.DataFrame:
    """
    Extract data from a CSV file and return a pandas DataFrame.

    Args:
        file_path (str): The full path to the CSV file.

    Returns:
        pl.DataFrame: The data as a DataFrame.
    """
    try:
        df = pl.read_csv(file_path)
        logger.info(f"CSV file loaded: {file_path} with {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV {file_path}: {e}")
        raise


def extract_json(file_path: str) -> pl.DataFrame:
    """
    Extract data from a JSON file and return a pandas DataFrame.

    Args:
        file_path (str): The full path to the JSON file.

    Returns:
        pd.DataFrame: The data as a DataFrame.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json_file.read()

        # Fix trailing commas in JSON if they exist
        data_cleaned = re.sub(r',(\s*[\]}])', r'\1', data)
        data_json = json.loads(data_cleaned)
        df = pl.DataFrame(data_json)
        logger.info(f"JSON file loaded: {file_path} with {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"Error loading JSON {file_path}: {e}")
        raise
    