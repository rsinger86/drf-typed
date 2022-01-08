from typing import Any, Callable, Type, TypeVar

from typing_extensions import ParamSpec

from .parsed_type import ParsedType

P = ParamSpec("P")
T = TypeVar("T")


def instance_type(instance_type: Type[T]):
    def decorator(Cls: Callable[P, Any]) -> Callable[P, T]:
        return Cls

    return decorator
