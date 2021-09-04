from typing import List
from rest_framework import serializers
from rest_framework.fields import empty
from rest_typed_views.serializers.decorators import deserialized_type


@deserialized_type(str)
class CharField(serializers.CharField):
    def __init__(
        self,
        read_only: bool = False,
        write_only: bool = False,
        required: bool = None,
        default=empty,
        initial=empty,
        source: str = None,
        label: str = None,
        help_text: str = None,
        style=None,
        error_messages=None,
        validators=None,
        allow_null: bool = False,
    ):
        super().__init__(
            read_only=read_only,
            write_only=write_only,
            required=required,
            default=default,
            initial=initial,
            source=source,
            label=label,
            help_text=help_text,
            style=style,
            error_messages=error_messages,
            validators=validators,
            allow_null=allow_null,
        )
