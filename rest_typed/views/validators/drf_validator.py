from typing import Type, Union

from django.http import QueryDict
from rest_framework import serializers
from rest_framework.request import Request


class DrfValidator(object):
    def __init__(self, SerializerClass: Type[serializers.Serializer], request: Request):
        self.SerializerClass = SerializerClass
        self.request = request

    def run_validation(self, data: Union[dict, QueryDict]):
        if isinstance(data, QueryDict):
            data = data.dict()

        serializer = self.SerializerClass(data=data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        return serializer
