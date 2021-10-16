# Enabling Marshmallow, Pydantic Schemas <a id="enabling-3rd-party-validators"></a>

As an alternative to Django REST's serializers, you can annotate views with [Pydantic](https://pydantic-docs.helpmanual.io/) models or [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) schemas to have their parameters automatically validated and pass an instance of the Pydantic/Marshmallow class to your method/function.

To enable support for third-party libraries for complex object validation, modify your settings:

```python
DRF_TYPED_VIEWS = {
    "schema_packages": ["pydantic", "marshmallow"]
}
```

These third-party packages must be installed in your virtual environment/runtime.
