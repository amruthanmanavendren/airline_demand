import requests
from django.conf import settings

def summarize_text(text):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        summary = response.json()[0].get('summary_text', '')
        return summary.strip()
    except Exception as e:
        print("Hugging Face summarization failed:", e)
        return text  # fallback to raw text
