import inspect
from rest_framework.fields import empty

from rest_framework.request import Request
from rest_typed.views.param_settings import ParamSettings
from rest_typed.views.params import (
    BodyParam,
    CurrentUserParam,
    HeaderParam,
    PassThruParam,
    PathParam,
    QueryParam,
)

from rest_typed.views.utils import (
    get_default_value,
    get_explicit_param_settings,
    is_explicit_request_param,
    is_implicit_body_param,
    is_implicit_request_param,
)


class ViewParamFactory(object):
    @classmethod
    def make(cls, param: inspect.Parameter, request: Request, path_args: dict):
        explicit_settings = get_explicit_param_settings(param)
        default = get_default_value(param)

        if explicit_settings:
            if explicit_settings.param_type == "path":
                key = explicit_settings.source or param.name
                raw_value = path_args.get(key, empty)
                return PathParam(param, request, settings=explicit_settings, raw_value=raw_value)
            elif explicit_settings.param_type == "body":
                return BodyParam(param, request, settings=explicit_settings)
            elif explicit_settings.param_type == "header":
                return HeaderParam(param, request, settings=explicit_settings)
            elif explicit_settings.param_type == "current_user":
                return CurrentUserParam(param, request, settings=explicit_settings)
            elif explicit_settings.param_type == "query_param":
                return QueryParam(param, request, settings=explicit_settings)
            raise Exception("Could not determine typed view param!")
        elif is_explicit_request_param(param):
            return PassThruParam(request)
        elif param.name in path_args:
            return PathParam(
                param,
                request,
                settings=ParamSettings(param_type="path", default=default),
                raw_value=path_args.get(param.name),
            )
        elif is_implicit_body_param(param):
            return BodyParam(
                param, request, settings=ParamSettings(param_type="body", default=default)
            )
        elif is_implicit_request_param(param):
            return PassThruParam(request)
        else:
            return QueryParam(
                param,
                request,
                settings=ParamSettings(param_type="query_param", default=default),
            )
