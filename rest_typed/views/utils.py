import inspect
import operator
from functools import reduce
from typing import Any, Optional

from rest_framework.fields import empty
from rest_framework.request import Request

from .param_settings import ParamSettings
from rest_typed.utils import inspect_complex_type


def get_nested_value(dic: dict, path: str, fallback=None) -> Any:
    try:
        return reduce(operator.getitem, path.split("."), dic)
    except (TypeError, KeyError, ValueError):
        return fallback


def get_default_value(param: inspect.Parameter) -> Any:
    if (
        not is_default_used_to_pass_settings(param)
        and param.default is not inspect.Parameter.empty
    ):
        return param.default
    return empty


def is_default_used_to_pass_settings(param: inspect.Parameter) -> bool:
    return get_explicit_param_settings(param) is not None


def get_explicit_param_settings(param: inspect.Parameter) -> Optional[ParamSettings]:
    try:
        param_type = param.default.param_type
        return param.default
    except AttributeError:
        return None


def is_implicit_body_param(param: inspect.Parameter) -> bool:
    t = inspect_complex_type(param.annotation)
    return t is not None


def is_explicit_request_param(param: inspect.Parameter) -> bool:
    return param.annotation is Request


def is_implicit_request_param(param: inspect.Parameter) -> bool:
    return param.name == "request" and param.annotation is inspect.Parameter.empty


def find_request(original_args: list) -> Request:
    for arg in original_args:
        if isinstance(arg, Request):
            return arg
    raise Exception("Could not find request in args:" + str(original_args))
