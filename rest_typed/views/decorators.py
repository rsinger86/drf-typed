import inspect
from typing import Any, Callable, Dict, List

from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_typed.views.utils import find_request

from .param_factory import ParamFactory


def wraps_drf(view):
    def _wraps_drf(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__name__ = view.__name__
        wrapper.__module__ = view.__module__
        wrapper.renderer_classes = getattr(
            view, "renderer_classes", APIView.renderer_classes
        )
        wrapper.parser_classes = getattr(view, "parser_classes", APIView.parser_classes)
        wrapper.authentication_classes = getattr(
            view, "authentication_classes", APIView.authentication_classes
        )
        wrapper.throttle_classes = getattr(
            view, "throttle_classes", APIView.throttle_classes
        )
        wrapper.permission_classes = getattr(
            view, "permission_classes", APIView.permission_classes
        )
        return wrapper

    return _wraps_drf


def transform_view_params(
    view_func: Callable, request: Request, path_args: dict
) -> List[Any]:
    typed_params = [
        p for n, p in inspect.signature(view_func).parameters.items() if n != "self"
    ]

    # List[Parameter] -> see docs: https://docs.python.org/3/library/inspect.html#inspect.Parameter

    validated_params = []
    errors: Dict[str, Any] = {}

    for param in typed_params:
        p = ParamFactory.make(param, request, path_args)
        value, error = p.validate_or_error()

        if error:
            errors.update(error)
        else:
            validated_params.append(value)

    if len(errors) > 0:
        raise ValidationError(errors)

    return validated_params


def prevalidate(view_func, for_method: bool = False):
    arg_info = inspect.getfullargspec(view_func)

    if arg_info.varargs is not None or arg_info.varkw is not None:
        raise Exception(
            f"{view_func.__name__}: variable-length argument lists and dictionaries cannot be used with typed views"
        )

    if for_method:
        error_msg = "For typed methods, 'self' must be passed as the first arg with no annotation"

        if (
            len(arg_info.args) < 1
            or arg_info.args[0] != "self"
            or "self" in arg_info.annotations
        ):
            raise Exception(error_msg)


def typed_api_view(methods):
    def wrap_validate_and_render(view):
        prevalidate(view)

        @api_view(methods)
        @wraps_drf(view)
        def wrapper(*original_args, **original_kwargs):
            original_args = list(original_args)
            request = find_request(original_args)
            transformed = transform_view_params(view, request, original_kwargs)
            return view(*transformed)

        return wrapper

    return wrap_validate_and_render


def typed_action(**action_kwargs):
    def wrap_validate_and_render(view):
        prevalidate(view, for_method=True)

        @action(**action_kwargs)
        @wraps_drf(view)
        def wrapper(*original_args, **original_kwargs):
            original_args = list(original_args)
            request = find_request(original_args)
            selfy = original_args.pop(0)
            transformed = transform_view_params(view, request, original_kwargs)
            return view(selfy, *transformed)

        return wrapper

    return wrap_validate_and_render
