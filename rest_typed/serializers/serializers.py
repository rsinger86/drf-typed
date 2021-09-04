from typing import Any
from typing import get_type_hints
from rest_typed_views.serializers import field_factory

from rest_framework import serializers
from rest_framework.serializers import empty


class TypedSerializerMetaClass(serializers.SerializerMetaclass):
    def __new__(cls, clsname, bases, attrs) -> Any:
        newclass = super(TypedSerializerMetaClass, cls).__new__(cls, clsname, bases, attrs)
        attr_name_to_type_hint = get_type_hints(newclass)
        declared_fields: dict = getattr(newclass, "_declared_fields")

        for attr_name, type_hint in attr_name_to_type_hint.items():
            if attr_name not in declared_fields and attr_name in attr_name_to_type_hint:
                type_hint = attr_name_to_type_hint[attr_name]

                default_value = (
                    getattr(newclass, attr_name) if hasattr(newclass, attr_name) else empty
                )

                declared_fields[attr_name] = field_factory.construct(type_hint, default_value)
                delattr(newclass, attr_name)

        return newclass


class TypedSerializerAttrFieldsMixin(object):
    def __getattr__(self, name: str) -> Any:
        if name not in self.fields.keys():
            raise AttributeError(f"{name} does not exist.")

        if not hasattr(self, "_validated_data"):
            msg = "You must call `.is_valid()` before accessing de-serialized attributes."
            raise AssertionError(msg)

        validated_data: dict = self.validated_data

        if name in validated_data:
            return validated_data[name]
        else:
            raise AttributeError(f"{name} does not exist.")


class ModelSerializer(
    TypedSerializerAttrFieldsMixin, serializers.ModelSerializer, metaclass=TypedSerializerMetaClass
):
    pass


class Serializer(
    TypedSerializerAttrFieldsMixin, serializers.Serializer, metaclass=TypedSerializerMetaClass
):
    pass
