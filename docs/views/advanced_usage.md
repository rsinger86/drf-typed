# Advanced Usage

## Overview

For more advanced use cases, you can explicitly declare how each parameter's value is sourced from the request -- from the query parameters, path, body or headers -- as well as define additional validation rules. You import a class named after the request element that is expected to hold the value and assign it to the parameter's default.

```python
from rest_typed_views import typed_api_view, Query, Path

@typed_api_view(["GET"])
def list_documents(year: date = Path(), title: str = Query(default=None)):
    # ORM logic here...
```

In this example, `year` is required and must come from the URL path and `title` is an optional query parameter because the `default` is set. This is similar to Django REST's [serializer fields](https://www.django-rest-framework.org/api-guide/fields/#core-arguments): passing a default implies that the filed is not required.

```python
from rest_typed_views import typed_api_view, Header

@typed_api_view(["GET"])
def get_cache_header(cache: str = Header()):
    # ORM logic here...
```

In this example, `cache` is required and must come from the headers.

## Additional Validation Rules

You can use the request element class (`Query`, `Path`, `Body`, `Header`) to set additional validation constraints. You'll find that these keywords are consistent with Django REST's serializer fields.

```python
from rest_typed_views import typed_api_view, Query, Path

@typed_api_view(["GET"])
def search_restaurants(
    year: date = Path(),
    rating: int = Query(default=None, min_value=1, max_value=5)
):
    # ORM logic here...


@typed_api_view(["GET"])
def get_document(id: str = Path(format="uuid")):
    # ORM logic here...


@typed_api_view(["GET"])
def search_users(
    email: str = Query(default=None, format="email"),
    ip_address: str = Query(default=None, format="ip"),
):
    # ORM logic here...
```

View a [full list](#supported-types-and-validator-rules) of supported types and additional validation rules.

## Nested Body Fields

Similar to how `source` is used in Django REST to control field mappings during serialization, you can use it to specify the exact path to the request data.

```python
from pydantic import BaseModel
from rest_typed_views import typed_api_view, Query, Path

class Document(BaseModel):
    title: str
    body: str

"""
    POST
    {
        "strict": false,
        "data": {
            "title": "A Dark and Stormy Night",
            "body": "Once upon a time"
        }
    }
"""
@typed_api_view(["POST"])
def create_document(
    strict_mode: bool = Body(source="strict"),
    item: Document = Body(source="data")
):
    # ORM logic here...
```

You can also use dot-notation to source data multiple levels deep in the JSON payload.

## List Validation

For the basic case of list validation - validating types within a comma-delimited string - declare the type to get automatic validation/coercion:

```python
from rest_typed_views import typed_api_view, Query

@typed_api_view(["GET"])
def search_movies(item_ids: List[int] = [])):
    print(item_ids)

# GET /movies?items_ids=41,64,3
# [41, 64, 3]
```

But you can also specify `min_length` and `max_length`, as well as the `delimiter` and specify additional rules for the child items -- think Django REST's [ListField](https://www.django-rest-framework.org/api-guide/fields/#listfield).

Import the generic `Param` class and use it to set the rules for the `child` elements:

```python
from rest_typed_views import typed_api_view, Query, Param

@typed_api_view(["GET"])
def search_outcomes(
    scores: List[int] = Query(delimiter="|", child=Param(min_value=0, max_value=100))
):
    # ORM logic ...

@typed_api_view(["GET"])
def search_message(
    recipients: List[str] = Query(min_length=1, max_length=10, child=Param(format="email"))
):
    # ORM logic ...
```

## Accessing the Request Object

You probably won't need to access the `request` object directly, as this package will provide its relevant properties as view arguments. However, you can include it as a parameter annotated with its type and it will be injected:

```python
from rest_framework.request import Request
from rest_typed_views import typed_api_view

@typed_api_view(["GET"])
def search_documens(request: Request, q: str = None):
    # ORM logic ...
```

## Interdependent Query Parameter Validation

Often, it's useful to validate a combination of query parameters - for instance, a `start_date` shouldn't come after an `end_date`. You can use complex schema object (Pydantic or Marshmallow) for this scenario. In the example below, `Query(source="*")` is instructing an instance of `SearchParamsSchema` to be populated/validated using all of the query parameters together: `request.query_params.dict()`.

```python
from marshmallow import Schema, fields, validates_schema, ValidationError
from rest_typed_views import typed_api_view

class SearchParamsSchema(Schema):
    start_date = fields.Date()
    end_date = fields.Date()

    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["start_date"] >= data["end_date"]:
            raise ValidationError("end_date must come after start_date")

@typed_api_view(["GET"])
def search_documens(search_params: SearchParamsSchema = Query(source="*")):
    # ORM logic ...
```

## (Simple) Access Control

You can apply some very basic access control by applying some validation rules to a view parameter sourced from the `CurrentUser` request element class. In the example below, a `ValidationError` will be raised if the `request.user` is not a member of either `super_users` or `admins`.

```python
    from my_pydantic_schemas import BookingSchema
    from rest_typed_views import typed_api_view, CurrentUser

    @typed_api_view(["POST"])
    def create_booking(
        booking: BookingSchema,
        user: User = CurrentUser(member_of_any=["super_users", "admins"])
    ):
        # Do something with the request.user
```

Read more about the [`Current User` request element class](#current-user-keywords).
