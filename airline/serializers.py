from rest_framework import serializers
from .models import Person
from .models import Flight, Location, Seats

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id','name', 'number','password']

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = "__all__"
