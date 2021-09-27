from collections import OrderedDict
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID

from pytz import UTC
from rest_framework import serializers
from rest_framework.test import APITestCase
from rest_typed.serializers import TModelSerializer, TSerializer
from test_project.testapp.models import Movie


class SerializerTests(APITestCase):
    def test_add_boolean_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            released: bool

        movie = MovieSerializer(data={"released": True})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.released, True)
        self.assertTrue(isinstance(movie.fields["released"], serializers.BooleanField))

    def test_add_date_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            release_date: date

        movie = MovieSerializer(data={"release_date": "2021-01-01"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.release_date, date(2021, 1, 1))
        self.assertTrue(isinstance(movie.fields["release_date"], serializers.DateField))

    def test_add_datetime_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            release_date: datetime

        movie = MovieSerializer(data={"release_date": "2013-01-29T12:34:56.000000Z"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.release_date, datetime(2013, 1, 29, 12, 34, 56, tzinfo=UTC))
        self.assertTrue(isinstance(movie.fields["release_date"], serializers.DateTimeField))

    def test_add_float_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            rating: Optional[float]
            genre: str
            title: str

        movie = MovieSerializer(
            data={"title": "Best Movie Ever.", "rating": 1.0, "genre": "comedy"}
        )

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.rating, 1.0)
        self.assertTrue(isinstance(movie.fields["rating"], serializers.FloatField))

    def test_add_int_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            rating: int

        movie = MovieSerializer(data={"rating": 8})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.rating, 8)
        self.assertTrue(isinstance(movie.fields["rating"], serializers.IntegerField))

    def test_add_char_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            title: str

        movie = MovieSerializer(data={"title": "Wizard of Oz"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.title, "Wizard of Oz")
        self.assertTrue(isinstance(movie.fields["title"], serializers.CharField))

    def test_add_time_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            showtime: time

        movie = MovieSerializer(data={"showtime": "15:00"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.showtime, time(15, 0))
        self.assertTrue(isinstance(movie.fields["showtime"], serializers.TimeField))

    def test_add_duration_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            length: timedelta

        movie = MovieSerializer(data={"length": "1 02:21:00"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.length, timedelta(days=1, seconds=8460))
        self.assertTrue(isinstance(movie.fields["length"], serializers.DurationField))

    def test_add_uuid_field_from_type_hint(self):
        class MovieSerializer(TSerializer):
            id: UUID

        movie = MovieSerializer(data={"id": "de305d54-75b4-431b-adb2-eb6b9e546013"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(str(movie.id), "de305d54-75b4-431b-adb2-eb6b9e546013")
        self.assertTrue(isinstance(movie.fields["id"], serializers.UUIDField))

    def test_add_choice_field_from_type_hint(self):
        class Genre(Enum):
            comedy = "comedy"
            drama = "drama"

        class MovieSerializer(TSerializer):
            genre: Genre

        movie = MovieSerializer(data={"genre": "comedy"})

        movie.is_valid(raise_exception=True)
        self.assertEqual(movie.genre, "comedy")

        self.assertTrue(isinstance(movie.fields["genre"], serializers.ChoiceField))

        self.assertEqual(
            movie.fields["genre"].choices, OrderedDict([("comedy", "comedy"), ("drama", "drama")])
        )
