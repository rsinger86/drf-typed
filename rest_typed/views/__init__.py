from typing import Any
from .decorators import typed_action, typed_api_view
from .param_settings import ParamSettings


def Query(*args, **kwargs) -> Any:
    return ParamSettings("query_param", *args, **kwargs)


def Path(*args, **kwargs) -> Any:
    return ParamSettings("path", *args, **kwargs)


def CurrentUser(*args, **kwargs) -> Any:
    return ParamSettings("current_user", *args, **kwargs)


def Body(*args, **kwargs) -> Any:
    return ParamSettings("body", *args, **kwargs)


def Header(*args, **kwargs) -> Any:
    return ParamSettings("header", *args, **kwargs)


def Param(*args, **kwargs) -> Any:
    return ParamSettings(*args, **kwargs)
