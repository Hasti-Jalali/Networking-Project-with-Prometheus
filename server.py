import socket
from prometheus_client import Gauge, start_http_server
import json
import threading

HOST = "127.0.0.1"
PORT = 8080


gauge0 = Gauge('memory_usage', 'Description of Memory_Usage', ['client_number'])
gauge1 = Gauge('disk_usage', 'Description of Disk_Usage', ['client_number'])
gauge2 = Gauge('cpu_percent', 'Description of CPU_Percent', ['client_number'])

def client_thread_handler(conn, addr, client_number):
    print(f"Client Number {client_number} Connected, {addr}")

    try:
        while True:
            msg = conn.recv(1024).decode('UTF-8')

            print(f"{msg}")
            client_metrics = json.loads(msg)

            gauge0.labels(f"client_{client_number}").set(client_metrics[0])
            
            gauge1.labels(f"client_{client_number}").set(client_metrics[1])

            gauge2.labels(f"client_{client_number}").set(client_metrics[2])
    except Exception as e:
        print(f'Client Number {client_number} Dissconnected!')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server {HOST}:{PORT} is ON")

    client_number = 1
    start_http_server(8100)

    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=client_thread_handler, args=(conn, addr,client_number))
        client_thread.start()
        client_number += 1
