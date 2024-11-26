
'''
import requests

# URL zu der API oder Webseite, von der du Daten abrufen möchtest
url = "http://127.0.0.1:7860/"

# Optionale Parameter, die du an die Anfrage anhängen kannst
params = {
    "key1": "value1",
    "key2": "value2"
}

try:
    # HTTP GET Anfrage senden
    response = requests.get(url, params=params)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        print("Anfrage erfolgreich!")
        print("Antwortdaten:", response)  # Wenn die Antwort JSON-Daten enthält
    else:
        print(f"Fehler: Statuscode {response.status_code}")
        print("Antwort:", response.text)
except requests.RequestException as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
print()

'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PORT = 8080 # Portnummer
HOST = "localhost"  # Server-Host (kann auch "0.0.0.0" für alle Interfaces sein)
COUNT = 0

# Server-Handler definieren
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # GET-Anfragen behandeln
    def do_GET(self):
        global COUNT
        self.send_response(200)  # HTTP-Statuscode: 200 OK
        self.send_header("Content-type", "text/html")  # Header setzen
        self.end_headers()  # Header abschließen

        # Antwortinhalt senden
        path_liegend = "D:/STUDIUM/Semester_4.5/WP_Mobile_Health/WP_MH/daten/liegend.json"
        with open(path_liegend, 'r') as file:
            data = json.load(file)
            response_content = str(COUNT) #json.dumps(data)
            self.wfile.write(response_content.encode("utf-8"))  # Inhalt schreiben
            COUNT += 1

# Server-Konfiguration
def run_server():
    global HOST, PORT # ?!? Warum global?
    server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    print(f"Server läuft auf http://{HOST}:{PORT}")
    server.serve_forever()  # Server starten

if __name__ == "__main__":
    run_server()