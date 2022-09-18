import socket
import time
import psutil
import json

HOST = '127.0.0.1'
PORT = 8080

while True:
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print(f'Connected to Server {HOST}:{PORT}')

        counter = 0

        while True:

            # https://pypi.org/project/psutil/3.4.2/
            v_memory = psutil.virtual_memory()
            memory_used = v_memory[2]
            disk_used = psutil.disk_usage('/')[3]
            cpu_prcnt = psutil.cpu_percent(interval=1)
            
            metrics = [memory_used, disk_used, cpu_prcnt]
            message = json.dumps(metrics)      

            s.send(message.encode('UTF-8'))

            print(f"Message Number {counter} Sent to Server")
            counter += 1
            time.sleep(2)

    except Exception as e:
        print(e)

        result = input("We Lost the Connection to Server, if you would like to reconnect enter 1, otherwise enter 0: ")
        if result == '1':
            continue
        else:
            break
    