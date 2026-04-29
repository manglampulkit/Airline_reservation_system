from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('flights/', views.get_flights),
    path('newflight/', views.add_flight),
    path('locations/', views.locations),
    path('search/', views.search_flights),
    path('book/', views.book_flight),
]
