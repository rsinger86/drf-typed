# Auto-Generated Serializer Fields

This package provides the following classes:

- `rest_typed.serializers.TSerializer`
- `rest_typed.serializers.TModelSerializer`

They are drop-in replacements for Django REST Framework's `serializers.Serializer` and `serializers.ModelSerializer` classes.

You can use type annotations as shorthand for declaring serializer fields, similar to how the popular library [Pydantic](https://pydantic-docs.helpmanual.io/) enforces type hints at runtime for data validation.

DRF's [core field arguments](https://www.django-rest-framework.org/api-guide/fields/#core-arguments) of `required`, `default` and `allow_null` map cleanly to Python's attribute type hints.

If you only need to specify those qualities, in addition to the type, you can use annotations instead of field declarations:

## Simple Example

```python
from datetime import date
from rest_typed.serializers import TSerializer


class BookingSerializer(TSerializer):
    start_date: date
    end_date: date
    number_of_people: int = None

"""
Same as:

class BookingSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    number_of_people = serializers.IntegerField(default=None)
"""
```

This approach works well for simple cases, but when you need more complex validation, such as enforcing value ranges or character length, it's best to use standard DRF fields.

## Enum & Lists Example

```python
from datetime import date
from rest_typed.serializers import TSerializer

class Genre(Enum):
    comedy = "comedy"
    drama = "drama"


class MovieSerializer(TSerializer):
    release_date: date
    genre: Genre
    cast: List[str]

"""
Same as:

class MovieSerializer(serializers.Serializer):
    release_date = serializers.DateField()
    genre = serializers.ChoiceField(choices=["comedy", "drama"])
    cast = serializers.ListField(child=serializers.CharField())
"""
```

## typing.Literal Example

```python
from datetime import date
from rest_typed.serializers import TSerializer


class MovieSerializer(TSerializer):
    release_date: date
    genre: Literal["comedy", "drama"]
    cast: List[str]

"""
Same as:

class MovieSerializer(serializers.Serializer):
    release_date = serializers.DateField()
    genre = serializers.ChoiceField(choices=["comedy", "drama"])
    cast = serializers.ListField(child=serializers.CharField())
"""
```
