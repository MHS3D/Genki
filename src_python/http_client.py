
import requests
import calc
import json
import time

JSON_DATA = []
RUNNING = True
INTERVAL = 1 #seconds

class SimpleHTTPRequest():
    # GET-Anfragen behandeln
    def get(self, url_path):
        global JSON_DATA
        try:
            # HTTP GET Anfrage senden
            response = requests.get(url_path, params=None)

            # Überprüfen, ob die Anfrage erfolgreich war
            if response.status_code == 200:
                print("Anfrage erfolgreich!")
                byte_content = response.content
                string_content = byte_content.decode('utf-8') # Bytes zu String umwandeln (UTF-8 Dekodierung)
                json_content = json.loads(string_content) # String zu JSON umwandeln
                accel, gyro = calc.read_values(json_content)
                accel = calc.delete_mean(accel)
                gyro = calc.delete_mean(gyro)
                JSON_DATA = calc.preparing_json(JSON_DATA, accel, gyro)
                # JSON-Daten in eine Datei schreiben
                with open("daten.json", "w", encoding="utf-8") as file:
                    json.dump(JSON_DATA, file, indent=4, ensure_ascii=False)  # JSON in Datei speichern
                print("JSON-Daten wurden in 'daten.json' gespeichert.")
            else:
                print(f"Fehler: Statuscode {response.status_code}")
                print("Antwort:", response.text)
        except requests.RequestException as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
        print()
        
def run_client(url_path):
    global RUNNING, INTERVAL
    client = SimpleHTTPRequest()
    while RUNNING:
        client.get(url_path)
        time.sleep(INTERVAL)