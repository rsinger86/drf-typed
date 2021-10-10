# Django REST Framework - Typed

## Overview

[![Package version](https://badge.fury.io/py/drf-typed-views.svg)](https://pypi.python.org/pypi/drf-typed-views)
[![Python versions](https://img.shields.io/pypi/status/drf-typed-views.svg)](https://img.shields.io/pypi/status/drf-typed-views.svg/)

This project extends [Django Rest Framework](https://www.django-rest-framework.org/) to allow use of Python's type annotations for automatically validating/casting view parameters and augmenting serializers with typed attributes and annotation-generated fields.

Deriving automatic behavior from type annotations has become increasingly popular with the FastAPI and Django Ninja frameworks. The goal of this project is to provide these benefits to the DRF ecosystem.

- View inputs are individually declared, not buried inside all-encompassing `request` objects.
- Type annotations can replace repetitive validation/sanitization code.
- Simple serializers can have their fields auto-generated from annotations
- Validated serializer data can be accessed from attributes, with their types known to the IDE
- [Pydantic](https://pydantic-docs.helpmanual.io/) models and [Marshmallow](https://marshmallow.readthedocs.io) schemas are compatible types for view parameters. Annotate your POST/PUT functions with them to automatically validate incoming request bodies.
- Advanced validators for more than just the type: `min_value`/`max_value` for numbers
- Validate string formats: `email`, `uuid` and `ipv4/6`; use Python's native `Enum` for "choices" validation

## Quick example - views

```python
from rest_typed.views import typed_api_view

@typed_api_view(["GET"])
def get_users(registered_on: date = None, groups: List[int] = None, is_staff: bool = None):
    print(registered_on, groups, is_staff)
```

GET `/users/registered/?registered_on=2019-03-03&groups=4,5&is_staff=yes`<br>

```python
# Status code: 200
date(2019, 3, 3)   [4, 5]  True
```

GET `/users/?registered_on=9999&groups=admin&is_staff=maybe`<br>

```python
# Status code: 400 / ValidationError raised
{
  "registered_on": "'9999' is not a valid date",
  "groups": "'admin' is not a valid integer",
  "is_staff": "'maybe' is not a valid boolean"
}
```

## Quick example - serializers
