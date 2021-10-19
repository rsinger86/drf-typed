from datetime import date
from typing import List
from rest_framework import serializers
from test_project.testapp.models import Movie
from rest_framework.serializers import ModelSerializer
from rest_typed.serializers import TSerializer
from rest_framework import serializers


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "rating", "genre"]


class BookingSerializer(TSerializer):
    start_date = serializers.DateField()
    first_name: str
    last_name: str


class MovieSerializer(TSerializer):
    release_date: date
    cast: List[str]


booking = BookingSerializer(
    {"start_date": "2021-10-01", "first_name": "Fred", "last_name": "Rogers"}
)

booking.is_valid()

booking.start_date
