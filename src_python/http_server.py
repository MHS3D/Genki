from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PATH = "daten.json"
PATH_UHR = "liegend.json"

# Server-Handler definieren
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # GET-Anfragen behandeln
    def do_GET(self):
        global PATH
        self.send_response(200)  # HTTP-Statuscode: 200 OK
        self.send_header("Content-type", "text/html")  # Header setzen
        self.end_headers()  # Header abschließen
        try:
            # Antwortinhalt senden
            with open(PATH, 'r') as file:
                data = json.load(file)
                response_content = json.dumps(data)
                self.wfile.write(response_content.encode("utf-8"))  # Inhalt schreiben
        except FileNotFoundError:
            response_content = "keine Daten Vorhanden"
            self.wfile.write(response_content.encode("utf-8"))

# Server-Konfiguration
def run_server(host,port):
    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    print(f"Server läuft auf http://{host}:{port}")
    server.serve_forever()  # Server starten

############################################################################################################################
############################################################################################################################
############################################################################################################################
# Server-Handler UHR definieren
class SimpleHTTPRequestHandlerUhr(BaseHTTPRequestHandler):
    # GET-Anfragen behandeln
    def do_GET(self):
        global PATH_UHR
        self.send_response(200)  # HTTP-Statuscode: 200 OK
        self.send_header("Content-type", "text/html")  # Header setzen
        self.end_headers()  # Header abschließen

        # Antwortinhalt senden
        with open(PATH_UHR, 'r') as file:
            data = json.load(file)
            response_content = json.dumps(data)
            self.wfile.write(response_content.encode("utf-8"))  # Inhalt schreiben

# Server-Konfiguration
def run_server_uhr(host,port):
    server = HTTPServer((host, port), SimpleHTTPRequestHandlerUhr)
    print(f"Uhr Test Server läuft auf http://{host}:{port}")
    server.serve_forever()  # Server starten