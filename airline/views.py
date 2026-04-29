from django.shortcuts import render
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, FlightSerializer, LocationSerializer
import uuid
from .models import Person,Flight,Location,Seats
from django.views.decorators.csrf import csrf_exempt

#REGISTER USER

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User registered successfully",
            "data": serializer.data
        })
    return Response(serializer.errors, status=400)

#LOGIN USER

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    if request.method=="POST":
        name = request.data.get("name")
        password = request.data.get("password")

        try:
            person = Person.objects.get(name = name, password = password)
            token = str(uuid.uuid4())
            person.token = token
            person.save()

            return Response({
                "message": "Login successful",
                "token": token
            })

        
        except Person.DoesNotExist:
            return Response({"error": "Invalid name or number"}, status=400)

    return Response({"message": "POST only"}, status=405)

#LOGOUT USER

@api_view(['GET'])
def logout_user(request):
    token = request.GET.get("token")
    if not token:
        return Response({"error": "Token required"}, status=400)
    try:
        person = Person.objects.get(token = token)
        person.token = ""
        person.save()
        return Response({"message": "Logout successful"})
    
    except Person.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)
    
#TO VIEW LOCATIONS

@api_view(['GET'])
def locations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)

#TO ADD FLIGHTS

@api_view(['POST'])
def add_flight(request):
    serializer = FlightSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Flight Added successfully",
            "data": serializer.data
        })
    return Response(serializer.errors, status=400)

#TO VIEW FLIGHTS

@api_view(['GET'])
def get_flights(request):
    flights = Flight.objects.all()
    serializer = FlightSerializer(flights, many=True)
    return Response(serializer.data)

#TO SEARCH FLIGHTS

@api_view(['POST'])
def search_flights(request):
    if request.method=="POST":
        origin = request.data.get("origin")
        destination = request.data.get("destination")
        seats = int(request.data.get("seats"))
        date = request.data.get("date")
        seat_class = request.data.get("class")

        flights = Flight.objects.all()

        if origin:
            flights = flights.filter(origin__iexact=origin)
        
        if destination:
            flights = flights.filter(destination__iexact=destination)
        
        if date:
            flights = flights.filter(departure_time__date=date)

        booked_counts = Seats.objects.filter(
            date=date,
            seat_class=seat_class
        ).values('flight_no').annotate(total_booked=Count('id'))

        booked_dict = {
            item['flight_no']: item['total_booked']
            for item in booked_counts
        }
        
        available_flights = []

         # Match flight_no
        for flight in flights:
            booked = booked_dict.get(flight.flight_no, 0)

            if seat_class == "economy":
                total = flight.total_economy_seats
            else:
                total = flight.total_business_seats

            available = total - booked

            if available >= seats:
                available_flights.append(flight)

        if available_flights:
            serializer = FlightSerializer(available_flights, many=True)
            return Response(serializer.data)
        
    #CONNECTING FLIGHTS
        
        first_leg = Flight.objects.filter(origin__iexact=origin)

        connecting_flights = []

        for f1 in first_leg:
            layover = f1.destination

            booked_f1 =Seats.objects.filter(
                flight_no=f1.flight_no,
                date = date,
                seat_class= seat_class
            ).count()

            if seat_class == "economy":
                total_f1 = f1.economy_seats
            else:
                total_f1 = f1.business_seats

            if (total_f1-booked_f1)<seats:
                continue 

            second_leg = Flight.objects.filter(origin__iexact = layover, 
                            destination__iexact = destination)
            
            for f2 in second_leg:

                booked_f2 =Seats.objects.filter(
                    flight_no=f2.flight_no,
                    date = date,
                    seat_class= seat_class
                ).count()

                if seat_class == "economy":
                    total_f2 = f2.economy_seats
                else:
                    total_f2 = f2.business_seats
                
                if (total_f2 - booked_f2) >= seats:
                    connecting_flights.append({
                        "first_flight": f1.flight_no,
                        "second_flight": f2.flight_no,
                        "via": layover
                    })
        
        return Response(connecting_flights)
    
#BOOKING LOGIC

@api_view(['POST'])
def book_flight(request):
    flight_no = request.data.get("flight_no")
    date = request.data.get("date")
    seat_class = request.data.get("class")
    passengers = request.data.get("passengers", [])
    token = request.data.get("token")

    if seat_class not in ["economy", "business"]:
        return Response({"error": "Invalid class"})

    if not passengers:
        return Response({"error": "No passengers provided"})

    try:
        flight = Flight.objects.get(flight_no=flight_no)
    except Flight.DoesNotExist:
        return Response({"error": "Flight not found"})

    for p in passengers:
        Seats.objects.create(
            name=p.get("name"),
            age=p.get("age"),
            flight_no=flight_no,
            date=date,
            seat_class=seat_class,
            token = token
        )

    return Response({
        "message": "Booking successful",
        "flight_no": flight_no,
        "passengers_booked": len(passengers)
    })




        

        

        






