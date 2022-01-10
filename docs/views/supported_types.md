# Supported Types and Validator Rules

## Overview

The following native Python types are supported. Depending on the type, you can pass additional validation rules to the request element class (`Query`, `Path`, `Body`). You can think of the type combining with the validation rules to create a Django REST serializer field on the fly -- in fact, that's what happens behind the scenes.

## str

Additional arguments:

- `max_length` Validates that the input contains no more than this number of characters.
- `min_length` Validates that the input contains no fewer than this number of characters.
- `trim_whitespace` (bool; default `True`) Whether to trim leading and trailing white space.
- `format` Validates that the string matches a common format; supported values:
  - `email` validates the text to be a valid e-mail address.
  - `slug` validates the input against the pattern `[a-zA-Z0-9_-]+`.
  - `uuid` validates the input is a valid UUID string
  - `url` validates fully qualified URLs of the form `http://<host>/<path>`
  - `ip` validates input is a valid IPv4 or IPv6 string
  - `ipv4` validates input is a valid IPv4 string
  - `ipv6` validates input is a valid IPv6 string
  - `file_path` validates that the input corresponds to filenames in a certain directory on the filesystem; allows all the same keyword arguments as Django REST's [`FilePathField`](https://www.django-rest-framework.org/api-guide/fields/#filepathfield)

Some examples:

```python
from rest_typed import typed_api_view, Query

@typed_api_view(["GET"])
def search_users(email: str = Query(format='email')):
    # ORM logic here...
    return Response(data)

@typed_api_view(["GET"])
def search_shared_links(url: str = Query(default=None, format='url')):
    # ORM logic here...
    return Response(data)

@typed_api_view(["GET"])
def search_request_logs(ip_address: str = Query(default=None, format='ip')):
    # ORM logic here...
    return Response(data)
```

## int

Additional arguments:

- `max_value` Validate that the number provided is no greater than this value.
- `min_value` Validate that the number provided is no less than this value.

An example:

```python
from rest_typed import typed_api_view, Query

@typed_api_view(["GET"])
def search_products(inventory: int = Query(min_value=0)):
    # ORM logic here...
```

## float

Additional arguments:

- `max_value` Validate that the number provided is no greater than this value.
- `min_value` Validate that the number provided is no less than this value.

An example:

```python
from rest_typed import typed_api_view, Query

@typed_api_view(["GET"])
def search_products(price: float = Query(min_value=0)):
    # ORM logic here...
```

## Decimal

Additional arguments:

- `max_value` Validate that the number provided is no greater than this value.
- `min_value` Validate that the number provided is no less than this value.
- .. even more ... accepts the same arguments as [Django REST's `DecimalField`](https://www.django-rest-framework.org/api-guide/fields/#decimalfield)

## bool

View parameters annotated with this type will validate and coerce the same values as Django REST's `BooleanField`, including but not limited to the following:

```python
    true_values = ["yes", 1, "on", "y", "true"]
    false_values = ["no", 0, "off", "n", "false"]
```

## datetime

Additional arguments:

- `input_formats` A list of input formats which may be used to parse the date-time, defaults to Django's `DATETIME_INPUT_FORMATS` settings, which defaults to `['iso-8601']`
- `default_timezone` A `pytz.timezone` of the timezone. If not specified, falls back to Django's `USE_TZ` setting.

## date

Additional arguments:

- `input_formats` A list of input formats which may be used to parse the date, defaults to Django's `DATETIME_INPUT_FORMATS` settings, which defaults to `['iso-8601']`

## time

Additional arguments:

- `input_formats` A list of input formats which may be used to parse the time, defaults to Django's `TIME_INPUT_FORMATS` settings, which defaults to `['iso-8601']`

## timedelta

Validates strings of the format `'[DD] [HH:[MM:]]ss[.uuuuuu]'` and converts them to a `datetime.timedelta` instance.

Additional arguments:

- `max_value` Validate that the input duration is no greater than this value.
- `min_value` Validate that the input duration is no less than this value.

## List

Validates strings of the format `'[DD] [HH:[MM:]]ss[.uuuuuu]'` and converts them to a `datetime.timedelta` instance.

Additional arguments:

- `min_length` Validates that the list contains no fewer than this number of elements.
- `max_length` Validates that the list contains no more than this number of elements.
- `child` Pass keyword constraints via a `Param` instance to to validate the members of the list.

An example:

```python
from rest_typed import typed_api_view, Param, Query

@typed_api_view(["GET"])
def search_contacts(emails: List[str] = Query(max_length=10, child=Param(format="email"))):
    # ORM logic here...
```

## Enum

Validates that the value of the input is one of a limited set of choices. Think of this as mapping to a Django REST [`ChoiceField`](https://www.django-rest-framework.org/api-guide/fields/#choicefield).

An example:

```python
from rest_typed import typed_api_view, Query

class Straws(str, Enum):
    paper = "paper"
    plastic = "plastic"

@typed_api_view(["GET"])
def search_straws(type: Straws = None):
    # ORM logic here...
```

## typing.Literal

As an alternative to `Enum`, `typing.Literal` can validate that the value of the input is one of a limited set of choices. Think of this as mapping to a Django REST [`ChoiceField`](https://www.django-rest-framework.org/api-guide/fields/#choicefield).

An example:

```python
from typing import Literal

@typed_api_view(["GET"])
def search_straws(type: Literal["paper", "plastic"] = None):
    # ORM logic here...
```

## Django REST Framework Serializers

You can annotate view parameters with Django Rest serializers to validate request data and pass an instance of the serializer to the view.

```python
from rest_framework import serializers
from rest_typed import typed_api_view

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField(read_only=True)

"""
    POST
    {
        "email": "mscott@paperco.com",
        "content": "great job team!",
    }
"""
@typed_api_view(["POST"])
def create_comment(comment: CommentSerializer):
    # is_valid() automatically called.
    # ready to access comment.validated_data
```

## DRF Typed - TSerializers

You can annotate view parameters with DRF Typed's TSerializers to validate request data and pass an instance of the serializer to the view.

```python
from rest_typed.serializers import TSerializer
from rest_typed import typed_api_view
from datetime import datetime

class CommentSerializer(TSerializer):
    email: str
    content: str
    created: datetime = serializers.DateTimeField(read_only=True)

"""
    POST
    {
        "email": "mscott@paperco.com",
        "content": "great job team!",
    }
"""
@typed_api_view(["POST"])
def create_comment(comment: CommentSerializer):
    # is_valid() automatically called.
    # ready to access comment.email and comment.content
```

## pydantic.BaseModel

You can annotate view parameters with [Pydantic models](https://pydantic-docs.helpmanual.io/) to validate request data and pass an instance of the model to the view.

```python
from pydantic import BaseModel
from rest_typed import typed_api_view, Query

class User(BaseModel):
    id: int
    name: str
    signup_ts: datetime = None
    friends: List[int] = []

"""
    POST
    {
        "id": 24529782,
        "name": "Michael Scott",
        "friends": [24529782]
    }
"""
@typed_api_view(["POST"])
def create_user(user: User):
    # now have a user instance (assuming ValidationError wasn't raised)
```
