from typing import Any, Callable, TypeVar, Type
from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


""" def typed_field(compatible_types):
    def decorator(Cls: Callable[P, Any]) -> Callable[P, Any]:
        Cls._compatible_types = compatible_types
        return Cls

    return decorator
 """


def deserialized_type(deserialized_type: Type[T]):
    def decorator(Cls: Callable[P, Any]) -> Callable[P, T]:
        return Cls

    return decorator
