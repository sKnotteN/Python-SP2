"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# Importer dei offentlige bibloteka
import socket
import pickle
import time


# Set nokre variablar som skal vere lett tilgjengelege
s = None
s_ip = None


# Vent på at ein klient skal kople til på satt ip og port, returner 'Connected' tilkopling og klient ip på tilkopling
def set_info(server_ip, port):
    global s
    global s_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_ip = (server_ip, port)
    try:
        s.connect(s_ip)
        return 'Connected'
    except OSError:
        return 'No server found'


# Send ein beskjed til serveren. Bruk pickle til og enkelt sende variablar
def send_message(message):
    msg = pickle.dumps(message)
    while True:
        try:
            s.sendall(msg)
            break
        except OSError:
            break


# Vent på ein melding frå server. Decode meldingen med pickle og returner meldingen
def receive():
    data = None
    while True:
        try:
            data = s.recv(1024)
        except OSError:
            return None
        finally:
            if data:
                data = pickle.loads(data)
                return data


# Stop tilkoplinga
def close_connection():
    s.close()


# set_info('169.254.135.140', 2000)
set_info('10.243.186.144', 5000)

for i in range(1, 10):
    send_message((100, 100))
    time.sleep(0.5)
