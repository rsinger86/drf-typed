from typing import Any, Dict, List, Optional, Union
from rest_typed.serializers import CharField, Serializer, ModelSerializer
from rest_framework.test import APITestCase
from test_project.testapp.models import Movie
from rest_framework import serializers


class SerializerTests(APITestCase):
    def test(self):
        class MovieSerializer(ModelSerializer):
            title: str = CharField(allow_null=True)
            rating: Optional[float] = None
            # actors: Optional[List[Optional[int]]] = []

            class Meta:
                model = Movie
                fields = ["id", "title", "rating", "genre"]

        movie = MovieSerializer(
            None, data={"title": "Best Movie Ever.", "rating": 1.0, "genre": "comedy"}
        )
        movie.is_valid(raise_exception=True)
        print("OUT")
        print(movie.rating)
        # print(movie.title)
