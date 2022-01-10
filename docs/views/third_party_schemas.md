# Enabling Pydantic Schemas <a id="enabling-3rd-party-validators"></a>

As an alternative to Django REST's serializers, you can annotate views with [Pydantic](https://pydantic-docs.helpmanual.io/) models to have their parameters automatically validated and pass an instance of the Pydantic class to your method/function.

To enable support, modify your settings:

```python
DRF_TYPED_VIEWS = {
    "schema_packages": ["pydantic"]
}
```

These third-party packages must be installed in your virtual environment/runtime.
