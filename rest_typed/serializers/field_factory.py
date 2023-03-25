from datetime import date, datetime, time, timedelta
from enum import Enum
import inspect
from typing import Any
from uuid import UUID

from rest_framework import serializers
from rest_framework.serializers import empty
from rest_typed import ParsedType

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
}


def construct(hint: Any, default_value: Any = empty):
    parsed = ParsedType(hint)
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
    elif inspect.isclass(parsed.resolved_type) and issubclass(
        parsed.resolved_type, serializers.Serializer
    ):
        return parsed.resolved_type(**kwargs)
    elif parsed.hint_is_list and parsed.inner_list_type:
        list_item_type = parsed.inner_list_type.resolved_type

        if inspect.isclass(list_item_type) and issubclass(
            list_item_type, serializers.Serializer
        ):
            return list_item_type(many=True)
