from datetime import date, datetime, time, timedelta
from typing import Any, Type, Union
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
    def is_nullable(self) -> bool:
        """
        If the type is a union, and one is None,
        then it's nullable
        """
        if get_origin(self._hint) is Union:
            for union_hint in get_args(self._hint):
                if union_hint is type(None):
                    return True

        return False

    @property
    def is_list(self) -> bool:
        """
        Type is `list` or `List[T]`
        Or it's a nullable list: `Optional[list]` or `Optional[List[T]]`
        """
        if self._hint is list or get_origin(self._hint) is list:
            return True
        elif get_origin(self._hint) is Union:
            for union_hint in get_args(self._hint):
                if union_hint is list or get_origin(union_hint) is list:
                    return True

        return False

    @property
    def type(self) -> Any:
        if self.is_nullable:
            for union_hint in get_args(self._hint):
                if union_hint is not type(None):
                    return get_origin(union_hint) or union_hint
        elif self.is_list:
            return list
        else:
            return self._hint

    @property
    def inner_type(self) -> Union["ParsedType", Type[empty]]:
        if not self.is_list:
            return empty

        if self.is_nullable:
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
}


def construct(hint: Any, default_value: Any = empty):
    parsed = ParsedType(hint, default_value)
    kwargs = {"allow_null": parsed.is_nullable}

    if default_value is not empty:
        kwargs["default"] = default_value
    else:
        kwargs["required"] = True

    if parsed.type in FIELD_MAPPING:
        FieldClass = FIELD_MAPPING[parsed.type]
        return FieldClass(**kwargs)
