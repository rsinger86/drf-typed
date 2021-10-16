# Request Elements

## Overview

You can specify the part of the request that holds each view parameter by using default function arguments, for example:

```python
    from rest_typed_views import Body, Query

    @typed_api_view(["PUT"])
    def update_user(
        user: UserSchema = Body(),
        optimistic_update: bool = Query(default=False)
    ):
```

The `user` parameter will come from the request body and is required because no default is provided. Meanwhile, `optimistic_update` is not required and will be populated from a query parameter with the same name.

The core keyword arguments to these classes are:

- `default` the default value for the parameter, which is required unless set
- `source` if the view parameter has a different name than its key embedded in the request

Passing keywords for additional validation constraints is a _powerful capability_ that gets you _almost the same feature set_ as Django REST's flexible [serializer fields](https://www.django-rest-framework.org/api-guide/fields/). See a [complete list](#supported-types-and-validator-rule) of validation keywords.

## Query

Use the `source` argument to alias the parameter value and pass keywords to set additional constraints. For example, your query parameters can have dashes, but be mapped to a parameter that have underscores:

```python
    from rest_typed_views import typed_api_view, Query

    @typed_api_view(["GET"])
    def search_events(
        starting_after: date = Query(source="starting-after"),
        available_tickets: int = Query(default=0, min_value=0)
    ):
        # ORM logic here...
```

## Body

By default, the entire request body is used to populate parameters marked with this class (`source="*"`):

```python
    from rest_typed_views import typed_api_view, Body
    from my_pydantic_schemas import ResidenceListing

    @typed_api_view(["POST"])
    def create_listing(residence: ResidenceListing = Body()):
        # ORM logic ...
```

However, you can also specify nested fields in the request body, with support for dot notation.

```python
    """
        POST  /users/
        {
            "first_name": "Homer",
            "last_name": "Simpson",
            "contact": {
                "phone" : "800-123-456",
                "fax": "13235551234"
            }
        }
    """
    from rest_typed_views import typed_api_view, Body

    @typed_api_view(["POST"])
    def create_user(
        first_name: str = Body(source="first_name"),
        last_name: str = Body(source="last_name"),
        phone: str = Body(source="contact.phone", min_length=10, max_length=20)
    ):
        # ORM logic ...
```

## Path

Use the `source` argument to alias a view parameter name. More commonly, though, you can set additional validation rules for parameters coming from the URL path.

```python
    from rest_typed_views import typed_api_view, Query

    @typed_api_view(["GET"])
    def retrieve_event(id: int = Path(min_value=0, max_value=1000)):
        # ORM logic here...
```

## Header

Use the `Header` request element class to automatically retrieve a value from a header. Underscores in variable names are automatically converted to dashes.

```python
    from rest_typed_views import typed_api_view, Header

    @typed_api_view(["GET"])
    def retrieve_event(id: int, cache_control: str = Header(default="no-cache")):
        # ORM logic here...
```

If you prefer, you can explicitly specify the exact header key:

```python
    from rest_typed_views import typed_api_view, Header

    @typed_api_view(["GET"])
    def retrieve_event(id: int, cache_control: str = Header(source="cache-control", default="no-cache")):
        # ORM logic here...
```

## CurrentUser <a id="current-user-keywords"></a>

Use this class to have a view parameter populated with the current user of the request. You can even extract fields from the current user using the `source` option.

```python
    from my_pydantic_schemas import BookingSchema
    from rest_typed_views import typed_api_view, CurrentUser

    @typed_api_view(["POST"])
    def create_booking(booking: BookingSchema, user: User = CurrentUser()):
        # Do something with the request.user

    @typed_api_view(["GET"])
    def retrieve_something(first_name: str = CurrentUser(source="first_name")):
        # Do something with the request.user's first name
```

You can also pass some additional parameters to the `CurrentUser` request element class to implement simple access control:

- `member_of` (str) Validates that the current `request.user` is a member of a group with this name
- `member_of_any` (List[str]) Validates that the current `request.user` is a member of one of these groups

_Using these keyword validators assumes that your `User` model has a many-to-many relationship with `django.contrib.auth.models.Group` via `user.groups`._

An example:

```python
from django.contrib.auth.models import User
from rest_typed_views import typed_api_view, CurrentUser

@typed_api_view(["GET"])
def do_something(user: User = CurrentUser(member_of="admin")):
    # now have a user instance (assuming ValidationError wasn't raised)
```
