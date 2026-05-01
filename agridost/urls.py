
from django.contrib import admin
from django.urls import path, include
from airline.views import register_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('airline.urls')),
]
