# views.py
from django.views import View
from django.shortcuts import render
from django.conf import settings
import requests
from collections import Counter
from django.utils.dateparse import parse_date
from datetime import datetime

class FlightInsightView(View):
    def get(self, request):
        base_url = "http://api.aviationstack.com/v1/flights"
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        flight_details = []
        routes = []
        route_counter = Counter()
        route_name_map = {}

        # Default params
        params = {
            'access_key': settings.AVIATIONSTACK_API_KEY,
            'limit': 10,
        }

        # Optional date filter
        if start_date:
            params['flight_date'] = start_date  # AviationStack supports a single date only

        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            flights = data.get("data", [])
        except Exception as e:
            print("API error:", e)
            flights = []

        for f in flights:
            dep = f.get("departure", {})
            arr = f.get("arrival", {})
            flight_number = f.get("flight", {}).get("iata", "N/A")
            airline = f.get("airline", {}).get("name", "Unknown Airline")

            dep_code = dep.get("iata", "N/A")
            arr_code = arr.get("iata", "N/A")
            dep_name = dep.get("airport", dep_code)
            arr_name = arr.get("airport", arr_code)
            dep_time = dep.get("scheduled", "N/A")
            arr_time = arr.get("scheduled", "N/A")

            # Apply filters if present
            if source and source != dep_code:
                continue
            if destination and destination != arr_code:
                continue

            # If end_date is given, compare scheduled time
            if end_date and dep_time:
                flight_dt = parse_date(dep_time.split("T")[0])
                if not (parse_date(start_date) <= flight_dt <= parse_date(end_date)):
                    continue

            route_key = f"{dep_code} → {arr_code}"
            route_counter[route_key] += 1
            route_name_map[route_key] = f"{dep_name} → {arr_name}"

            flight_details.append({
                "flight_number": flight_number,
                "airline": airline,
                "from": f"{dep_name} ({dep_code})",
                "to": f"{arr_name} ({arr_code})",
                "departure_time": dep_time,
                "arrival_time": arr_time,
            })

        unique_routes = [
            f"{route_name_map[r]} ({count})"
            for r, count in route_counter.items()
        ]

        top_routes = route_counter.most_common(10)
        chart_data = {
            "labels": [r[0] for r in top_routes],   # route names
            "counts": [r[1] for r in top_routes],   # route frequencies
        }

        context = {
            "routes": unique_routes,
            "chart_data": chart_data,
            "flight_details": flight_details,
        }

        return render(request, 'flights/flight_insights.html', context)