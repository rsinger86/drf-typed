# Typed Serializers

This package provides the following classes:

- `rest_typed.serializers.TSerializer`
- `rest_typed.serializers.TModelSerializer`

They are drop-in replacements for Django REST Framework's `serializers.Serializer` and `serializers.ModelSerializer` classes.

## Auto-Generated Serializer Fields

You can use type annotations as shorthand for declaring serializer fields, similar to how the popular library [Pydantic](https://pydantic-docs.helpmanual.io/) enforces type hints at runtime for data validation.

This approach works well for simple cases, but when you need more complex validation, such as enforcing value ranges or character length, it's best to use DRF's fields.

DRF's [core field arguments](https://www.django-rest-framework.org/api-guide/fields/#core-arguments) of `required`, `default` and `allow_null` map cleanly to Python's attribute type hints.

If you only need to specify those qualities, in addition to the type, you can use annotations instead of field declarations:

### Simple Example

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

### Enum & Lists Example

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

## Typed/Direct Atrribute Access

When using `TSerializer` or `TModelSerializer` you also have direct access to validated field values after calling `is_valid()`:

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

movie = MovieSerializer({'release_date': '2021-10-10', 'genre': 'drama', 'cast': ['Steve Martin']})
movie.is_valid()

print(movie.cast)
# ['Steve Martin']
```

## IDE Integration

Classes are used to represent serializer fields, which can confuse IDEs into assuming that field values should be instances of those classes, rather than the value type that the class is responsible for validating and deserializing.

The project includes a set of type stubs copied from [typeddjango/django-stubs](https://github.com/typeddjango/django-stubs) (credit due to them for excellent work) and altered to indicate deserialized field types and address the problem stated above.

![IDE_1](/images/ide-integration-1.png)

This allows your IDE to know that `start_date` is of type `datetime.date`, even though a type annotation was not used.

![IDE_2](/images/ide-integration-2.png)
