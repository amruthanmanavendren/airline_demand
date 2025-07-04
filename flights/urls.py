from django.urls import path
from .views import FlightInsightView
from .views import FlightInsightView

urlpatterns = [
    path("flights/", FlightInsightView.as_view(), name="flight-insight"),
]