import inspect
from typing import Any, Tuple

from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field, empty
from rest_framework.request import Request
from rest_typed import ParsedType
from rest_typed.views.param_settings import ParamSettings
from rest_typed.views.utils import get_nested_value
from rest_typed.views.validator_factory import ValidatorFactory
from rest_typed.views.validators import CurrentUserValidator


class Param(object):
    def __init__(
        self,
        param: inspect.Parameter,
        request: Request,
        settings: ParamSettings,
        raw_value: Any = empty,
    ):
        self.param = param
        self.request = request
        self.settings = settings
        self.raw_value = raw_value
        self.parsed_type = ParsedType(self.param.annotation)

    def get_validator(self) -> Field:
        return ValidatorFactory.make(self.parsed_type, self.settings, self.request)

    def get_raw_value(self):
        raise Exception("Must implement in concrete class!")

    @property
    def source(self) -> str:
        return self.settings.source or self.param.name

    def validate_or_error(self) -> Tuple[Any, Any]:
        validator = self.get_validator()

        try:
            value = validator.run_validation(self.get_raw_value())
            return value, None
        except ValidationError as e:
            return None, {self.source: e.detail}


class QueryParam(Param):
    def get_raw_value(self):
        if self.settings.source == "*":
            raw = self.request.query_params.dict()
        else:
            key = self.settings.source or self.param.name
            raw = self.request.query_params.get(key, empty)
            raw = empty if raw == "" else raw

            if raw is not empty and self.parsed_type.resolved_type is list:
                raw = raw.split(self.settings.delimiter)

        return raw


class PathParam(Param):
    def get_raw_value(self):
        raw = self.raw_value
        return raw


class PassThruParam(object):
    def __init__(self, value: Any):
        self.value = value

    def validate_or_error(self) -> Tuple[Any, Any]:
        return self.value, None


class BodyParam(Param):
    def get_raw_value(self):
        if self.settings.source in ("*", None):
            return self.request.data
        return get_nested_value(self.request.data, self.settings.source, fallback=empty)


class HeaderParam(Param):
    def get_raw_value(self):
        headers = {
            str(key).lower(): value for key, value in self.request.headers.items()
        }

        if self.settings.source == "*":
            raw = headers
        else:
            if self.settings.source:
                key = self.settings.source
            else:
                key = self.param.name.replace("_", "-").lower()

            raw = headers.get(key)

        return raw


class CurrentUserParam(Param):
    def get_raw_value(self):
        if self.settings.source in ("*", None):
            return self.request.user

        obj = self.request.user

        for path in self.settings.source.split("."):
            if hasattr(obj, path):
                obj = getattr(obj, path)
            else:
                obj = None
                break

        return obj

    def validate_or_error(self) -> Tuple[Any, Any]:
        value = self.get_raw_value()
        generic_validator = self.get_validator()
        current_user_validator = CurrentUserValidator(self.settings)

        try:
            value = generic_validator.run_validation(value)
            current_user_validator.run_validation(self.request.user)
            return value, None
        except ValidationError as e:
            return None, {self.source: e.detail}
