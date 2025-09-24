"""
Contains all functions that are related to handling the .json files. Includes:
- converting nested data to flat dicts
- loading to context window
"""

import logging
logger = logging.getLogger(__name__)

import json

from os import listdir
from os.path import join

from config.constants import PARENT_FOLDER
from src.utils import ScoringContext

def load_json_files_into_context() -> None:
        load_flat_data_to_context()
        load_nested_data_to_context()


def load_flat_data_to_context() -> None:
    flat_dicts = listdir(join(PARENT_FOLDER, 'data'))

    for file_name in flat_dicts:
        if file_name.endswith('.json'):
            with open(join(PARENT_FOLDER, 'data', file_name), 'r', encoding="utf-8") as f:
                data = json.load(f)

            dict_name = file_name[:-5]
            setattr(ScoringContext, dict_name, data)


def load_nested_data_to_context() -> None:
    nested_dicts = listdir(join(PARENT_FOLDER, 'data', 'nested_data'))

    for file_name in nested_dicts:
        if file_name.endswith('.json'):
            with open(join(PARENT_FOLDER, 'data', 'nested_data', file_name), 'r', encoding="utf-8") as f:
                data = json.load(f)

            dict_name = file_name[:-5]

            flat_dict = nested_to_flat_dict(data)
            logger.debug(f"Converted nested dictionary {dict_name} to a flat dictionary.")
            setattr(ScoringContext, dict_name, flat_dict)


def nested_to_flat_dict(data: dict[str, dict]) -> dict[str, float]:
    flat_dict = {}

    for word, word_attrs in data.items():
        if word == "_comment":
            continue

        score = word_attrs["score"]
        variations = word_attrs["variations"]

        for variation in variations:
            flat_dict[variation] = score

        flat_dict[word] = score

    return flat_dict