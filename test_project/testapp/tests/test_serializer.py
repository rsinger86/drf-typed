from collections import OrderedDict
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import List, Literal, Optional
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
        self.assertEqual(
            movie.release_date, datetime(2013, 1, 29, 12, 34, 56, tzinfo=UTC)
        )
        self.assertTrue(
            isinstance(movie.fields["release_date"], serializers.DateTimeField)
        )

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

    def test_add_choice_field_from_enum_type_hint(self):
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
            movie.fields["genre"].choices,
            OrderedDict([("comedy", "comedy"), ("drama", "drama")]),
        )

    def test_add_choice_field_from_literal_type_hint(self):
        class PetSerializer(TSerializer):
            species: Literal["cat", "dog"]

        pet = PetSerializer(data={"species": "cat"})

        pet.is_valid(raise_exception=True)
        self.assertEqual(pet.species, "cat")

        self.assertTrue(isinstance(pet.fields["species"], serializers.ChoiceField))

        self.assertEqual(
            pet.fields["species"].choices,
            OrderedDict([("cat", "cat"), ("dog", "dog")]),
        )

        self.assertFalse(
            pet.fields["species"].allow_null,
        )

    def test_add_choice_field_from_optional_literal_type_hint(self):
        class PetSerializer(TSerializer):
            species: Optional[Literal["cat", "dog"]]

        # Check literal value allowed
        pet = PetSerializer(data={"species": "cat"})
        pet.is_valid(raise_exception=True)
        self.assertEqual(pet.species, "cat")

        # Check None is allowed
        pet = PetSerializer(data={"species": None})
        pet.is_valid(raise_exception=True)
        self.assertEqual(pet.species, None)

        # Check field constructed correctly
        self.assertTrue(isinstance(pet.fields["species"], serializers.ChoiceField))

        self.assertEqual(
            pet.fields["species"].choices,
            OrderedDict([("cat", "cat"), ("dog", "dog")]),
        )

        self.assertTrue(
            pet.fields["species"].allow_null,
        )

    def test_nested_serializer_from_type_hint_validation(self):
        class AuthorSerializer(TSerializer):
            name = serializers.CharField()

        class BookSerializer(TSerializer):
            author: AuthorSerializer

        book = BookSerializer(data={"author": {"name": "JK Rowling"}})
        book.is_valid(raise_exception=True)
        self.assertEqual(book.author.name, "JK Rowling")

    def test_many_nested_serializer_from_type_hint(self):
        class ChapterSerializer(TSerializer):
            title = serializers.CharField()
            word_count = serializers.IntegerField()

        class BookSerializer(TSerializer):
            chapters: List[ChapterSerializer]

        book = BookSerializer(data={"chapters": [{"title": "Intro", "word_count": 13}]})
        book.is_valid(raise_exception=True)

        self.assertEqual(len(book.chapters), 1)

        for chapter in book.chapters:
            self.assertEqual(chapter.title, "Intro")
            self.assertEqual(chapter.word_count, 13)

    def test_nested_serializer_from_type_hint_construction(self):
        class AuthorSerializer(TSerializer):
            name: str

        class BookSerializer(TSerializer):
            author: Optional[AuthorSerializer] = None

        book = BookSerializer(data={"author": {"name": "JK Rowling"}})
        self.assertEqual(book.fields["author"].allow_null, True)
        self.assertEqual(book.fields["author"].default, None)

        class BookSerializer(TSerializer):
            author: AuthorSerializer = None

        book = BookSerializer(data={"author": {"name": "JK Rowling"}})
        self.assertEqual(book.fields["author"].allow_null, False)
        self.assertEqual(book.fields["author"].default, None)
