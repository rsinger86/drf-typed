from enum import Enum
from inspect import isclass
from typing import Any, List, Literal, Type, Union

from django.conf import settings
from rest_framework.serializers import empty
from typing_extensions import get_args, get_origin


class ParsedType(object):
    _hint: Any

    def __init__(self, hint: Any):
        self._hint = hint

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
    def resolved_hint(self) -> Any:
        if self.is_optional:
            for union_hint in get_args(self._hint):
                if union_hint is not type(None):
                    return union_hint

        return self._hint

    @property
    def hint_is_list(self) -> bool:
        """
        Type is `list` or `List[T]`
        Or it's a nullable list: `Optional[list]` or `Optional[List[T]]`
        """
        return self.resolved_hint is list or get_origin(self.resolved_hint) is list

    @property
    def hint_is_literal(self) -> bool:
        return get_origin(self.resolved_hint) is Literal

    @property
    def hint_is_enum(self) -> bool:
        return isclass(self.resolved_hint) and issubclass(self.resolved_hint, Enum)

    @property
    def enum_values(self) -> List[Any]:
        if self.hint_is_enum:
            return [_.value for _ in self.resolved_hint]
        elif self.hint_is_literal:
            return [v for v in get_args(self.resolved_hint)]
        else:
            return []

    @property
    def resolved_type(self) -> Any:
        t = self.resolved_hint

        if self.hint_is_list:
            t = list
        elif self.hint_is_literal or self.hint_is_enum:
            t = Enum

        return t

    @property
    def inner_list_type(self) -> Union["ParsedType", Type[empty]]:
        if self.resolved_type is list and get_origin(self.resolved_hint) is list:
            return ParsedType(get_args(self.resolved_hint)[0])

        return empty
