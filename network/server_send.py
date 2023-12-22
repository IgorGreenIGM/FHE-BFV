import os
import socket

CLIENT_PORT = 5000
CLIENT_IP_ADDRESS = '192.168.56.1'

# send results to the client
print("Sending computed results file to the client")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect((CLIENT_IP_ADDRESS, CLIENT_PORT))   
while True: 
    filename = 'datas/results.zip'
    size = os.path.getsize(filename)
    sock.send(f'{size}'.encode())
    try: 
        fi = open(filename, "rb") 
        data = fi.read()
        if not data:
            break
        else:
            sock.sendall(data)
            break
        fi.close()

    except IOError: 
        break