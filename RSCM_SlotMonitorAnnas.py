import requests
import time
import random
from dotenv import load_dotenv
import os

from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import RequestException

# =========================
# CONFIG
# =========================

load_dotenv()

URL = os.getenv("RSCM_API")

# TANGGAL_AWAL = datetime.today().strftime("%Y-%m-%d")
# TANGGAL_AWAL = "2026-08-11"
# JUMLAH_HARI = 1

TANGGAL_AWAL = ["2026-08-18"]
JUMLAH_HARI = len(TANGGAL_AWAL)



DELAY_MIN = 1
DELAY_MAX = 2

BASE_PAYLOAD = {
    "appointment_date": TANGGAL_AWAL,
    "poli_id": os.getenv("POLI_ID")
}

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.9.0",
    "Connection": "close"
}

# =========================
# SESSION + RETRY
# =========================

session = requests.Session()

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"]
)

adapter = HTTPAdapter(max_retries=retry)

session.mount("https://", adapter)

# =========================
# Function
# =========================
def kirim_telegram(pesan):

    TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    
    for i in range (5):
        try:
            pesan = pesan + f"Telegram berhasil dalam retry ke-{i}"
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                params={
                    "chat_id": CHAT_ID,
                    "text": pesan
                },
                timeout=30
            )

            response.raise_for_status()

            print(f"Telegram berhasil dalam retry ke-{i}")
            return

        except RequestException as e:
            print (f"retry ke-{i+1}: {e}")
            time.sleep(5)
        
    print(f"Telegram gagal: {e}")

# =========================
# LOOP
# =========================



for i in range(JUMLAH_HARI):
    
    start_date = datetime.strptime(TANGGAL_AWAL[i], "%Y-%m-%d")

    bank_date = []
    bank_error_date = []

    current_date = start_date 
    tanggal = current_date.strftime("%Y-%m-%d")

    payload = BASE_PAYLOAD.copy()
    payload["appointment_date"] = tanggal

    try:

        response = session.post(
            URL,
            json=payload,
            headers=HEADERS,
            timeout=15
        )

        data = response.json()

        success = data.get("success", False)
        message = data.get("message", "")

        if success:
            # kirim_telegram(
            #     f"🚨 ADA SLOT!\nTanggal: {tanggal}"
            # )
            bank_date.append(tanggal)
            print(f"{tanggal} -> [ADA SLOT]")

        else:
            print(f"{tanggal} -> [x] ({message})")

    except Exception as e:
        bank_error_date.append(f"{tanggal}: {e}")
        print(f"{tanggal} -> ERROR: {e}")

    delay = random.uniform(DELAY_MIN, DELAY_MAX)

    # print(f"Menunggu {delay:.2f} detik...\n")

    time.sleep(delay)
print("selesai...")

curr_hour = datetime.now().strftime("%d-%m-%y %H:%M")
TANGGAL_AKHIR = (
    start_date+timedelta(days = JUMLAH_HARI -1)
).strftime("%Y-%m-%d")

report = f"""
daily report
last_check: {curr_hour}

list_check: 
{TANGGAL_AWAL}


"""

report_ada_slot = "ADA SLOT A3! \n"

if bank_date:
    report_ada_slot += report
    report = report_ada_slot  
    
    report += "slot tersedia \n\n"
    for tgl in bank_date:
        report += f"-) {tgl}\n"
else:
    report += "\n tidak ada slot tersedia \n"

if bank_error_date:
    report += "\n ERROR \n"
    
    for err in bank_error_date:
        report += f"x {err}\n"


print(report)

kirim_telegram(report)

# print("kirim telegram selesai....")
    



# import requests

# TOKEN = "8920592883:AAHZcl6j4mz23uVYrd1nkgNu-OzGkS0aalc"
# CHAT_ID = "5382745861"

# response = requests.get(
#     f"https://api.telegram.org/bot{TOKEN}/sendMessage",
#     params={
#         "chat_id": CHAT_ID,
#         "text": "Tes dari Python"
#     }
# )

# print(response.json())