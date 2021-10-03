from typing import Any, Callable, Dict, List, Type, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def instance_type(instance_type: Type[T]):
    def decorator(Cls: Callable[P, Any]) -> Callable[P, T]:
        return Cls

    return decorator
