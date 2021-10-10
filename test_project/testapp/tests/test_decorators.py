import inspect
from unittest.mock import MagicMock, patch

from pydantic import BaseModel
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.test import APITestCase
from rest_typed.views import Body, CurrentUser, ParamSettings, Path, Query
from rest_typed.views.decorators import transform_view_params
from rest_typed.views.params import (
    BodyParam,
    CurrentUserParam,
    PassThruParam,
    PathParam,
    QueryParam,
)


class FakeUser(object):
    username: str

    def __init__(self, username: str = "bob"):
        self.username = username


class DecoratorTests(APITestCase):
    def fake_request(self, data={}, query_params: dict = None, user: FakeUser = None):
        return MagicMock(
            data=data, query_params=query_params or {}, user=user or FakeUser()
        )

    def get_params(self, func):
        return list(inspect.signature(func).parameters.values())

    def test_transform_view_params_succeeds(self):
        def example_function(id: int, q: str):
            return

        request = self.fake_request(query_params={"q": "cats"})

        result = transform_view_params(example_function, request, {"id": "1"})
        self.assertEqual(result, [1, "cats"])

    def test_transform_view_params_throws_error(self):
        def example_function(id: int, q: str):
            return

        request = self.fake_request(query_params={})

        with self.assertRaises(ValidationError) as context:
            transform_view_params(example_function, request, {"id": "one"})

        self.assertTrue("A valid integer is required" in str(context.exception))
        self.assertTrue("This field is required" in str(context.exception))

    def test_get_view_param_if_explicit_settings(self):
        def example_function(name_from_body: str = Body(source="name")):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(data={"name": "MJ"}),
            {"pk": "1"},
        )

        self.assertEqual(result, ["MJ"])

    def test_get_view_param_if_explicit_request_param(self):
        def example_function(request: Request):
            return

        request = self.fake_request()
        result = transform_view_params(example_function, request, {})
        self.assertEqual(result, [request])

    def test_get_view_param_if_implicit_path_param(self):
        def example_function(pk: int):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(),
            {"pk": "1"},
        )

        self.assertEqual(result, [1])

    def test_get_view_param_if_implicit_body_param(self):
        class User(BaseModel):
            id: int
            name = "John Doe"

        def example_function(user: User):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(data={"id": 1, "name": "Bob"}),
            {"id": "1"},
        )

        self.assertEqual(result, [User(id=1, name="Bob")])

    def test_get_view_param_if_implicit_query_param(self):
        def example_function(q: str):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(query_params={"q": "mysearch"}),
            {"id": "1"},
        )

        self.assertEqual(result, ["mysearch"])

    def test_build_explicit_param_for_query(self):
        def example_function(q: str = Query()):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(query_params={"q": "HI"}),
            {},
        )

        self.assertEqual(result, ["HI"])

    def test_build_explicit_param_for_path(self):
        def example_function(id: str = Path()):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(),
            {"id": 12},
        )

        self.assertEqual(result, ["12"])

    def test_build_explicit_param_for_body(self):
        def example_function(d: dict = Body()):
            return

        result = transform_view_params(
            example_function,
            self.fake_request(data={"a": "b"}),
            {"id": 12},
        )

        self.assertEqual(result, [{"a": "b"}])

    def test_build_explicit_param_for_current_user(self):
        def example_function(user: FakeUser = CurrentUser()):
            return

        bob = FakeUser(username="bobdylan")

        result = transform_view_params(
            example_function,
            self.fake_request(user=bob),
            {"id": 12},
        )

        self.assertEqual(result, [bob])
