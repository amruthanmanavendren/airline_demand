# flights/huggingface_summary.py

import requests
from django.conf import settings

def summarize_text_with_huggingface(text):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": text,
        "options": {"wait_for_model": True}
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return result[0]["summary_text"] if result else "No summary available."
