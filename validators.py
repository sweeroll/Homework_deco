"""Валидаторы входящих и исходящих данных."""
import json
import os
import re
from typing import Dict, Any, Tuple

import jsonschema

from custom_exceptions import GeneralVerificationError


def json_validator(json_str: str) -> bool:
    """Валидатор для json."""
    with open(os.path.join(os.getcwd(), 'schema.json'), 'r') as schema_file:
        json_schema = json.load(schema_file)
    try:
        json_data = json.loads(json_str)
        jsonschema.validate(instance=json_data, schema=json_schema)
    except (jsonschema.exceptions.ValidationError, json.decoder.JSONDecodeError) as e:
        raise GeneralVerificationError
    return True


def regex_validator(string: str) -> bool:
    """Валидатор для regex."""
    with open(os.path.join(os.getcwd(), 'schema.regex')) as schema_file:
        regex = schema_file.readline()
    if not re.match(regex, string):
        raise GeneralVerificationError
    return True


def default_validator(*args: Tuple[Any], **kwargs: Dict[Any, Any]) -> bool:
    """Стандартный."""
    return True
