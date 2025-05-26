
import os
import csv
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === EINSTELLUNGEN ===
SHEET_NAME = "tradelog_bot"
TAB_NAME = "Sheet1"
CREDENTIALS_FILE = "syrinksolar-a57f4a67fac8.json"
CSV_FILE = "tradelog.csv"

# === GOOGLE SHEETS LOGIN ===
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1pypd1rtOGedJ_xJZXJVuTADbfEAQvslhoIm6Wv_3EN8/edit")
    return sheet.worksheet(TAB_NAME)

# === CSV EINTRÄGE HOCHLADEN ===
def upload_trades_to_google_sheet():
    try:
        sheet = get_sheet()
        with open(CSV_FILE, newline="") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            for row in rows:
                if row:  # keine leeren Zeilen
                    sheet.append_row(row, value_input_option="RAW")
        print(f"✅ Hochgeladen: {len(rows)} Zeilen")
        # CSV leeren
        open(CSV_FILE, "w").close()
    except Exception as e:
        print("❌ Fehler beim Hochladen:", e)

# === 9 STUNDEN LOOP ===
if __name__ == "__main__":
    while True:
        upload_trades_to_google_sheet()
        print(f"⏳ Warte 9 Stunden bis zum nächsten Upload ({datetime.now().isoformat()})")
        time.sleep(9 * 60 * 60)
