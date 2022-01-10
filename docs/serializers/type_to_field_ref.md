# Type-to-Field Reference

Below is a complete mapping of how native type annotations can be used as shorthand to generate Django REST Framework's serializer fields.

| Type           | Field                     |
| -------------- | ------------------------- |
| bool           | serializers.BooleanField  |
| date           | serializers.DateField     |
| datetime       | serializers.DateTimeField |
| float          | serializers.FloatField    |
| int            | serializers.IntegerField  |
| str            | serializers.CharField     |
| time           | serializers.TimeField     |
| timedelta      | serializers.DurationField |
| UUID           | serializers.UUIDField     |
| Enum           | serializers.ChoiceField   |
| typing.Literal | serializers.ChoiceField   |
