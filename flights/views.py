import requests
from collections import Counter
import random
from django.conf import settings
from django.shortcuts import render
from django.views import View
from .huggingface_summary import summarize_text_with_huggingface


class FlightInsightView(View):
    def get(self, request):
        base_url = "http://api.aviationstack.com/v1/flights"
        params = {
            'access_key': settings.AVIATIONSTACK_API_KEY,
            'limit': 100,
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        flights = data.get("data", [])

        route_counter = Counter()
        flight_details = []

        for f in flights:
            dep = f.get("departure", {})
            arr = f.get("arrival", {})
            airline = f.get("airline", {})
            flight_info = f.get("flight", {})

            dep_code = dep.get("iata")
            arr_code = arr.get("iata")
            dep_name = dep.get("airport", "")
            arr_name = arr.get("airport", "")

            if not dep_code or not arr_code:
                continue

            route_label = f"{dep_code} → {arr_code} ({dep_name} → {arr_name})"
            route_counter[route_label] += 1

            price = random.randint(100, 1200)

            flight_details.append({
                "flight_number": flight_info.get("number", "N/A"),
                "airline": airline.get("name", "N/A"),
                "from": f"{dep_code} - {dep_name}",
                "to": f"{arr_code} - {arr_name}",
                "departure_time": dep.get("scheduled", "N/A"),
                "arrival_time": arr.get("scheduled", "N/A"),
                "price": price,
            })

        # Prepare chart data
        top_routes = route_counter.most_common(10)
        chart_data = {
            "labels": [r for r, _ in top_routes],
            "counts": [c for _, c in top_routes],
        }

        # AI summary from Hugging Face
        summary_input = "\n".join([f"{r}: {c} flights" for r, c in top_routes])
        try:
            summary = summarize_text_with_huggingface("Flight route trends:\n" + summary_input)
        except Exception:
            summary = "Could not generate AI summary."

        context = {
            "chart_data": chart_data,
            "routes": [r for r, _ in top_routes],
            "flight_details": flight_details,
            "summary": summary,
        }
        return render(request, 'flights/flight_insights.html', context)
