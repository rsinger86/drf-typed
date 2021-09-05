from typing import Any, Dict, List, Optional, Union
from rest_framework.test import APITestCase
from test_project.testapp.models import Movie

from rest_typed.serializers import TypedModelSerializer
from rest_framework import serializers

from django.db.models import Model


class TypedModel(Model):
    pass


class SerializerTests(APITestCase):
    def test(self):
        class MovieSerializer(TypedModelSerializer):
            title: str = serializers.CharField()
            rating: Optional[float] = None
            # email = fields.EmailField()
            # actors: Optional[List[Optional[int]]] = []

            class Meta:
                model = Movie
                fields = ["id", "title", "rating", "genre"]

        movie = MovieSerializer(
            None, data={"title": "Best Movie Ever.", "rating": 1.0, "genre": "comedy"}
        )

        movie.is_valid(raise_exception=True)
        print("OUT")
        print(movie.title)
        # print(movie.title)
