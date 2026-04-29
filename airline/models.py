from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    password = models.CharField(max_length=20, default="password123")
    token = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_no = models.CharField(max_length=20)
    origin = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    economy_seats = models.IntegerField(default = 60)
    business_seats = models.IntegerField(default = 30)
    economy_price = models.IntegerField()
    business_price = models.IntegerField()
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return self.flight_no

class Location(models.Model):
    city = models.CharField(max_length=50, unique=True)
    airport_code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f"{self.city} ({self.airport_code})"

class Seats(models.Model):
    flight_no = models.CharField()
    name = models.CharField()
    age = models.CharField()
    seat_class = models.CharField()
    date = models.DateField()