# Typed Views

## Simple Usage

For many cases, you can rely on implicit behavior for how different parts of the request (URL path variables, query parameters, body) map to the parameters of a view function/method.

The value of a view parameter will come from...

- the URL path if the path variable and the view argument have the same name, _or_:
- the request body if the view argument is annotated using a class from a supported library for complex object validation (Pydantic, MarshMallow), _or_:
- a query parameter with the same name

Unless a default value is given, the parameter is **required** and a [`ValidationError`](https://www.django-rest-framework.org/api-guide/exceptions/#validationerror) will be raised if not set.

## Basic GET Request

```python
urlpatterns = [
    url(r"^(?P<city>[\w+])/restaurants/", search_restaurants)
]

from rest_typed_views import typed_api_view

# Example request: /chicago/restaurants?delivery=yes
@typed_api_view(["GET"])
def search_restaurants(city: str, rating: float = None, offers_delivery: bool = None):
    restaurants = Restaurant.objects.filter(city=city)

    if rating is not None:
        restaurants = restaurants.filter(rating__gte=rating)

    if offers_delivery is not None:
        restaurants = restaurants.filter(delivery=offers_delivery)
```

In this example, `city` is required and must be its string. Its value comes from the URL path variable with the same name. The other parameters, `rating` and `offers_delivery`, are not part of the path parameters and are assumed to be query parameters. They both have a default value, so they are optional.

## Basic POST Request

```python
# urls.py
urlpatterns = [url(r"^(?P<city>[\w+])/bookings/", create_booking)]

# settings.py
DRF_TYPED_VIEWS = {"schema_packages": ["pydantic"]}

# views.py
from pydantic import BaseModel
from rest_typed_views import typed_api_view


class RoomEnum(str, Enum):
    double = 'double'
    twin = 'twin'
    single = 'single'


class BookingSchema(BaseModel):
    start_date: date
    end_date: date
    room: RoomEnum = RoomEnum.double
    include_breakfast: bool = False

# Example request: /chicago/bookings/
@typed_api_view(["POST"])
def create_booking(city: str, booking: BookingSchema):
    # do something with the validated booking...
```

In this example, `city` will again be populated using the URL path variable. The `booking` parameter is annotated using a supported complex schema class (Pydantic), so it's assumed to come from the request body, which will be read in as JSON, used to hydrate the Pydantic `BookingSchema` and then validated. If validation fails a `ValidationError` will be raised.
