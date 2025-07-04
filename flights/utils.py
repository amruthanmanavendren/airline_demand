import requests
from django.conf import settings

def summarize_text(text, model="facebook/bart-large-cnn"):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": text}

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()[0]['summary_text']
    else:
        return "Error in summarization"
