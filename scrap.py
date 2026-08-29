import os

poli_id = os.getenv("POLI_ID")

for p in poli_id:

    BASE_PAYLOAD = {
        "appointment_date": 0,
        "poli_id": p
    }
    print(BASE_PAYLOAD)