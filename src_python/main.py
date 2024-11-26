import threading
import http_server
import http_client

TEST = False # False wenn der Server der Uhr tatsächlich läuft

HOST_SERVER_UHR = "192.168.119.26"  # Server-Host Uhr
PORT_SERVER_UHR = 80 # Portnummer

URL_PATH_CLIENT = f"http://{HOST_SERVER_UHR}:{PORT_SERVER_UHR}/"

HOST_SERVER = "127.0.0.1"  # Server-Host
PORT_SERVER = 1234 # Portnummer

if __name__ == "__main__":
    if TEST:
        server_uhr_thread = threading.Thread(target=http_server.run_server_uhr, args=[HOST_SERVER_UHR,PORT_SERVER_UHR])
        server_uhr_thread.start()
    client_thread = threading.Thread(target=http_client.run_client, args=[URL_PATH_CLIENT])
    client_thread.start()
    server_thread = threading.Thread(target=http_server.run_server, args=[HOST_SERVER,PORT_SERVER])
    server_thread.start()