from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, Union
from rest_framework.request import Request

from rest_framework import serializers
from rest_framework.fields import empty
from rest_typed import ParsedType
from rest_typed.utils import inspect_complex_type
from rest_typed.views.param_settings import ParamSettings
from rest_typed.views.validators import (
    DefaultValidator,
    DrfValidator,
    PydanticValidator,
)


class ValidatorFactory(object):
    @classmethod
    def make_string_validator(cls, settings: ParamSettings):
        if settings.regex:
            return serializers.RegexField(
                settings.regex,
                default=settings.default,
                max_length=settings.max_length,
                min_length=settings.min_length,
            )

        if settings.format is None:
            return serializers.CharField(
                default=settings.default,
                max_length=settings.max_length,
                min_length=settings.min_length,
                trim_whitespace=settings.trim_whitespace,
            )

        if settings.format == "email":
            return serializers.EmailField(
                default=settings.default,
                max_length=settings.max_length,
                min_length=settings.min_length,
            )

        if settings.format == "slug":
            return serializers.SlugField(
                default=settings.default,
                max_length=settings.max_length,
                min_length=settings.min_length,
            )

        if settings.format == "url":
            return serializers.URLField(
                default=settings.default,
                max_length=settings.max_length,
                min_length=settings.min_length,
            )

        if settings.format == "uuid":
            return serializers.UUIDField(default=settings.default)

        if settings.format == "file_path":
            return serializers.FilePathField(
                default=settings.default,
                path=settings.path,
                match=settings.match,
                recursive=settings.recursive,
                allow_files=settings.allow_files,
                allow_folders=settings.allow_folders,
            )

        if settings.format == "ipv6":
            return serializers.IPAddressField(default=settings.default, protocol="IPv6")

        if settings.format == "ipv4":
            return serializers.IPAddressField(default=settings.default, protocol="IPv4")

        if settings.format == "ip":
            return serializers.IPAddressField(default=settings.default, protocol="both")

    @classmethod
    def make_list_validator(
        cls,
        inner_type: Union[ParsedType, empty],
        settings: ParamSettings,
        request: Request,
    ):
        options = {
            "min_length": settings.min_length,
            "max_length": settings.max_length,
            "allow_empty": settings.allow_empty,
            "default": settings.default,
        }
        if inner_type is not empty:
            options["child"] = ValidatorFactory.make(
                inner_type, settings.child or ParamSettings(), request
            )

        return serializers.ListField(**options)

    @classmethod
    def make(cls, parsed: ParsedType, settings: ParamSettings, request: Request) -> Any:

        if parsed.resolved_type is bool:
            return serializers.BooleanField(default=settings.default)
        elif parsed.resolved_type is str:
            return cls.make_string_validator(settings)
        elif parsed.resolved_type is int:
            return serializers.IntegerField(
                default=settings.default,
                max_value=settings.max_value,
                min_value=settings.min_value,
            )
        elif parsed.resolved_type is float:
            return serializers.FloatField(
                default=settings.default,
                max_value=settings.max_value,
                min_value=settings.min_value,
            )
        elif parsed.resolved_type is Decimal:
            return serializers.DecimalField(
                default=settings.default,
                max_digits=settings.max_digits,
                decimal_places=settings.decimal_places,
                coerce_to_string=settings.coerce_to_string,
                localize=settings.localize,
                rounding=settings.rounding,
                max_value=settings.max_value,
                min_value=settings.min_value,
            )
        elif parsed.resolved_type is datetime:
            return serializers.DateTimeField(
                default=settings.default,
                input_formats=settings.input_formats,
                default_timezone=settings.default_timezone,
            )
        elif parsed.resolved_type is date:
            return serializers.DateField(
                default=settings.default, input_formats=settings.input_formats
            )
        elif parsed.resolved_type is time:
            return serializers.TimeField(
                default=settings.default, input_formats=settings.input_formats
            )
        elif parsed.resolved_type is timedelta:
            return serializers.DurationField(default=settings.default)
        elif parsed.resolved_type is Enum:
            return serializers.ChoiceField(choices=parsed.enum_values)
        elif parsed.resolved_type is list:
            return cls.make_list_validator(parsed.inner_list_type, settings, request)
        else:
            complex_type = inspect_complex_type(parsed.resolved_type)

            if complex_type == "pydantic":
                return PydanticValidator(parsed.resolved_type)
            elif complex_type == "drf":
                return DrfValidator(parsed.resolved_type, request)

        return DefaultValidator(default=settings.default)
