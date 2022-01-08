from datetime import date, datetime, time, timedelta
from enum import Enum
from inspect import isclass
from typing import Any, List, Literal, Type, Union
from uuid import UUID

from rest_framework import serializers
from rest_framework.serializers import empty
from typing_extensions import get_args, get_origin


class ParsedType(object):
    _hint: Any
    _default: Any

    def __init__(self, hint: Any, default: Any):
        self._hint = hint
        self._default = default

    @property
    def is_optional(self) -> bool:
        """
        If the type is a union, and one is None, then it's nullable
        """
        if get_origin(self._hint) is Union:
            for union_hint in get_args(self._hint):
                if union_hint is type(None):
                    return True

        return False

    @property
    def hint(self) -> Any:
        if self.is_optional:
            for union_hint in get_args(self._hint):
                if union_hint is not type(None):
                    return union_hint

        return self._hint

    @property
    def is_list(self) -> bool:
        """
        Type is `list` or `List[T]`
        Or it's a nullable list: `Optional[list]` or `Optional[List[T]]`
        """
        return self.hint is list or get_origin(self.hint) is list

    @property
    def is_literal(self) -> bool:
        return get_origin(self.hint) is Literal

    @property
    def is_enum(self) -> bool:
        return isclass(self.hint) and issubclass(self.hint, Enum)

    @property
    def enum_values(self) -> List[Any]:
        if self.resolved_type is Enum:
            return [_.value for _ in self.hint]
        elif self.resolved_type is Literal:
            return [v for v in get_args(self.hint)]
        else:
            return []

    @property
    def resolved_type(self) -> Any:
        t = self.hint

        if self.is_list:
            t = list
        elif self.is_literal:
            t = Literal
        elif self.is_enum:
            t = Enum

        return t

    @property
    def inner_type(self) -> Union["ParsedType", Type[empty]]:
        if not self.is_list:
            return empty

        if self.is_optional:
            for union_hint in get_args(self._hint):
                if union_hint is type(None):
                    continue

                if get_origin(union_hint) is list:
                    return ParsedType(get_args(union_hint)[0], empty)

            return empty
        elif get_origin(self._hint) is list:
            return ParsedType(get_args(self._hint)[0], empty)
        else:
            return empty


FIELD_MAPPING = {
    bool: serializers.BooleanField,
    date: serializers.DateField,
    datetime: serializers.DateTimeField,
    # Decimal: serializers.DecimalField,
    float: serializers.FloatField,
    int: serializers.IntegerField,
    str: serializers.CharField,
    time: serializers.TimeField,
    timedelta: serializers.DurationField,
    UUID: serializers.UUIDField,
    Enum: serializers.ChoiceField,
    Literal: serializers.ChoiceField,
}


def construct(hint: Any, default_value: Any = empty):
    parsed = ParsedType(hint, default_value)
    kwargs = {"allow_null": parsed.is_optional}

    if default_value is not empty:
        kwargs["default"] = default_value
    else:
        kwargs["required"] = True

    if parsed.resolved_type in FIELD_MAPPING:
        FieldClass = FIELD_MAPPING[parsed.resolved_type]

        if FieldClass is serializers.ChoiceField:
            kwargs["choices"] = parsed.enum_values

        return FieldClass(**kwargs)
