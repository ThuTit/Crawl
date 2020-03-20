"""
Utility functions, helpers for Schema
"""
import json

import jsonschema
from jsonschema.exceptions import ValidationError

from support.decorators import memoize


def validate(instance, schema: dict) -> tuple:
    result = False
    message = None
    path = None

    try:
        jsonschema.validate(instance, schema)
        result = True
    except ValidationError as ex:
        message = ex.message
        path = '.'.join(ex.path)
    except Exception as ex:
        raise
    return result, message, path


@memoize
def get_api_schema(schema_path: str) -> dict:
    """
    Get api Schema
    :param schema_path:
    :return:
    """
    with open(schema_path, 'r') as fh:
        return json.loads(fh.read().strip())
