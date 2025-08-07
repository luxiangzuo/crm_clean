import requests

data = {
    "contact_id": "180426993137",
    "email": "emailmaria@hubspot.com",
    "first_name": "Maria"
}

response = requests.post("http://localhost:8000/hubspot/ai_followup_note", json=data)
print(response.json())
