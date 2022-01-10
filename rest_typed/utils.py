import inspect
from typing import Any, Literal, Optional

from django.conf import settings
from rest_framework import serializers


def inspect_complex_type(t: Any) -> Optional[Literal["drf", "pydantic"]]:
    if hasattr(settings, "DRF_TYPED_VIEWS"):
        enabled = settings.DRF_TYPED_VIEWS.get("schema_packages", [])
    else:
        enabled = []

    if "pydantic" in enabled:
        from pydantic import BaseModel as PydanticBaseModel

        if inspect.isclass(t) and issubclass(t, PydanticBaseModel):
            return "pydantic"

    if inspect.isclass(t) and issubclass(t, serializers.Serializer):
        return "drf"

    return None
