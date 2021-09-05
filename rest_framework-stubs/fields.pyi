import datetime
import uuid
from decimal import Decimal
from json import JSONDecoder, JSONEncoder
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Pattern,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.core.files.base import File
from django.db import models
from django.forms import ImageField as DjangoImageField
from rest_framework.validators import Validator

from rest_typed.utils.decorators import deserialized_type

_IN = TypeVar("_IN")  # Instance Type
_VT = TypeVar("_VT")  # Value Type
_DT = TypeVar("_DT")  # Data Type
_RP = TypeVar("_RP")  # Representation Type

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

_DefaultInitial = Union[_VT, Callable[[], _VT], None, _Empty]

class Field(Generic[_VT, _DT, _RP, _IN]):
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[_VT] = ...,
        initial: _DefaultInitial[_VT] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[_VT]]] = ...,
        allow_null: bool = ...,
    ): ...

@deserialized_type(bool)
class BooleanField(
    Field[
        bool,
        Union[str, bool, int],
        bool,
        Any,
    ]
): ...

@deserialized_type(Optional[bool])
class NullBooleanField(
    Field[
        Union[bool, None],
        Optional[Union[str, bool, int]],
        bool,
        Any,
    ]
):
    TRUE_VALUES: Set[Union[str, bool, int]] = ...
    FALSE_VALUES: Set[Union[str, bool, int, float]] = ...
    NULL_VALUES: Set[Union[str, None]] = ...

@deserialized_type(str)
class CharField(Field[str, str, str, Any]):
    allow_blank: bool = ...
    trim_whitespace: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[str]]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

@deserialized_type(str)
class EmailField(CharField): ...

@deserialized_type(str)
class RegexField(CharField):
    def __init__(
        self,
        regex: Union[str, Pattern],
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[str]]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

@deserialized_type(str)
class SlugField(CharField):
    def __init__(
        self,
        allow_unicode: bool = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[str]]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

@deserialized_type(str)
class URLField(CharField): ...

@deserialized_type(uuid.UUID)
class UUIDField(Field[uuid.UUID, Union[uuid.UUID, str, int], str, Any]):
    def __init__(
        self,
        *,
        format: Optional[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[uuid.UUID] = ...,
        initial: _DefaultInitial[uuid.UUID] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[uuid.UUID]]] = ...,
        allow_null: bool = ...,
    ): ...

class IPAddressField(CharField):
    def __init__(
        self,
        protocol: str = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[str]]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class IntegerField(Field[int, Union[float, int, str], int, Any]):
    def __init__(
        self,
        *,
        max_value: int = ...,
        min_value: int = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[int] = ...,
        initial: _DefaultInitial[int] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[int]]] = ...,
        allow_null: bool = ...,
    ): ...

class FloatField(Field[float, Union[float, int, str], str, Any]):
    def __init__(
        self,
        *,
        max_value: float = ...,
        min_value: float = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[float] = ...,
        initial: _DefaultInitial[float] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[float]]] = ...,
        allow_null: bool = ...,
    ): ...

class DecimalField(Field[Decimal, Union[int, float, str, Decimal], str, Any]):
    def __init__(
        self,
        max_digits: Optional[int],
        decimal_places: Optional[int],
        coerce_to_string: bool = ...,
        max_value: Union[Decimal, int, float] = ...,
        min_value: Union[Decimal, int, float] = ...,
        localize: bool = ...,
        rounding: Optional[str] = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Decimal] = ...,
        initial: _DefaultInitial[Decimal] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Decimal]]] = ...,
        allow_null: bool = ...,
    ): ...

class DateTimeField(Field[datetime.datetime, Union[datetime.datetime, str], str, Any]):
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Sequence[str] = ...,
        default_timezone: Optional[datetime.tzinfo] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.datetime] = ...,
        initial: _DefaultInitial[datetime.datetime] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[datetime.datetime]]] = ...,
        allow_null: bool = ...,
    ): ...

class DateField(Field[datetime.date, Union[datetime.date, str], str, Any]):
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Sequence[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.date] = ...,
        initial: _DefaultInitial[datetime.date] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[datetime.date]]] = ...,
        allow_null: bool = ...,
    ): ...

class TimeField(Field[datetime.time, Union[datetime.time, str], str, Any]):
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Sequence[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.time] = ...,
        initial: _DefaultInitial[datetime.time] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[datetime.time]]] = ...,
        allow_null: bool = ...,
    ): ...

class DurationField(Field[datetime.timedelta, Union[datetime.timedelta, str], str, Any]):
    def __init__(
        self,
        *,
        max_value: Union[datetime.timedelta, int, float] = ...,
        min_value: Union[datetime.timedelta, int, float] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.timedelta] = ...,
        initial: _DefaultInitial[datetime.timedelta] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[datetime.timedelta]]] = ...,
        allow_null: bool = ...,
    ): ...

class ChoiceField(
    Field[str, Union[str, int, Tuple[Union[str, int], Union[str, int, tuple]]], str, Any]
):
    def __init__(
        self,
        choices: Iterable[Any],
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Union[str, int]] = ...,
        initial: _DefaultInitial[Union[str, int]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Any]]] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
    ): ...

class MultipleChoiceField(
    ChoiceField,
    Field[
        str,
        Sequence[Union[str, int, Tuple[Union[str, int], Union[str, int]]]],
        Sequence[Union[str, Tuple[Union[str, int], Union[str, int]]]],
        Any,
    ],
):
    def __init__(
        self,
        choices: Iterable[Any],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Union[Set[Union[str, int]], Set[str], Set[int]]] = ...,
        initial: _DefaultInitial[Union[Set[Union[str, int]], Set[str], Set[int]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Any]]] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
        allow_empty: bool = ...,
    ): ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str,
        match: str = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        required: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Any]]] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
    ): ...

class FileField(
    Field[File, File, Union[str, None], Any]
):  # this field can return None without raising!
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[File] = ...,
        initial: _DefaultInitial[File] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[File]]] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
    ): ...

class ImageField(FileField):
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[File] = ...,
        initial: _DefaultInitial[File] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[File]]] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
        _DjangoImageField: Type[SupportsToPython] = ...,
    ): ...

@deserialized_type(List[Any])
class ListField(Field[List[Any], List[Any], List[Any], Any]):
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[List[Any]] = ...,
        initial: _DefaultInitial[List[Any]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[List[Any]]]] = ...,
        allow_null: bool = ...,
        *,
        child: Field = ...,
        allow_empty: bool = ...,
        max_length: int = ...,
        min_length: int = ...,
    ): ...

@deserialized_type(dict)
class DictField(Field[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any], Any]):
    child: Field = ...
    allow_empty: bool = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Dict[Any, Any]] = ...,
        initial: _DefaultInitial[Dict[Any, Any]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Dict[Any, Any]]]] = ...,
        allow_null: bool = ...,
        *,
        child: Field = ...,
        allow_empty: bool = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

@deserialized_type(dict)
class HStoreField(DictField):
    child: CharField = ...

@deserialized_type(dict)
class JSONField(
    Field[
        Union[Dict[str, Any], List[Dict[str, Any]]],
        Union[Dict[str, Any], List[Dict[str, Any]]],
        str,
        Any,
    ]
):
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Mapping[Any, Any]] = ...,
        initial: _DefaultInitial[Mapping[Any, Any]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Any]]] = ...,
        allow_null: bool = ...,
        *,
        binary: bool = ...,
        encoder: Optional[JSONEncoder] = ...,
        decoder: Optional[JSONDecoder] = ...,
    ): ...

@deserialized_type(Any)
class SerializerMethodField(Field):
    def __init__(
        self,
        method_name: str = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Any]]] = ...,
        allow_null: bool = ...,
    ): ...

class ModelField(Field):
    def __init__(
        self,
        model_field: models.Field,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Optional[Sequence[Validator[Any]]] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
    ): ...
