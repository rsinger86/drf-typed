from rest_framework import serializers
from rest_framework.fields import empty
from typing_extensions import get_type_hints

from rest_typed.serializers import field_factory


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class TSerializerMetaClass(serializers.SerializerMetaclass):
    def __new__(cls, clsname, bases, attrs):

        newclass = super(TSerializerMetaClass, cls).__new__(cls, clsname, bases, attrs)
        attr_name_to_type_hint = get_type_hints(newclass)
        declared_fields: dict = getattr(newclass, "_declared_fields")

        for attr_name, type_hint in attr_name_to_type_hint.items():
            if attr_name not in declared_fields:
                type_hint = attr_name_to_type_hint[attr_name]

                default_value = (
                    getattr(newclass, attr_name)
                    if hasattr(newclass, attr_name)
                    else empty
                )

                declared_fields[attr_name] = field_factory.construct(
                    type_hint, default_value
                )

                if hasattr(newclass, attr_name):
                    delattr(newclass, attr_name)

        return newclass


class TSerializerAttrFieldsMixin(object):
    def __getattr__(self, name: str):
        if name not in self.fields.keys():
            raise AttributeError(f"{name} does not exist.")

        if not hasattr(self, "_validated_data"):
            msg = (
                "You must call `.is_valid()` before accessing de-serialized attributes."
            )
            raise AssertionError(msg)

        validated_data: dict = self.validated_data

        if name not in validated_data:
            raise AttributeError(f"{name} does not exist.")

        field_instance = self.fields[name]
        field_data = validated_data[name]

        if isinstance(field_instance, TSerializerAttrFieldsMixin) and isinstance(
            field_data, dict
        ):
            field_data = AttrDict(**field_data)
        elif (
            isinstance(field_instance, serializers.ListSerializer)
            and isinstance(field_instance.child, TSerializerAttrFieldsMixin)
            and isinstance(field_data, list)
        ):
            field_data = [AttrDict(**data) for data in field_data]

        return field_data

    def asdict(self) -> dict:
        if not hasattr(self, "_validated_data"):
            msg = (
                "You must call `.is_valid()` before accessing de-serialized attributes."
            )
            raise AssertionError(msg)

        return self.validated_data


class TModelSerializer(
    TSerializerAttrFieldsMixin,
    serializers.ModelSerializer,
    metaclass=TSerializerMetaClass,
):
    pass


class TSerializer(
    TSerializerAttrFieldsMixin,
    serializers.Serializer,
    metaclass=TSerializerMetaClass,
):
    pass
