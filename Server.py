"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# https://automatetheboringstuff.com/chapter18/
# https://www.youtube.com/watch?v=2BXr9U6ZL8Y


# Importer dei offentlige bibloteka
import socket
import pickle
import pyautogui


# Set nokre variablar som skal vere lett tilgjengelege
s = None
s_ip = None
connection = None
client_ip = None
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

# Lagrer informasjonen som skal bli brukt i variabler. Lag ein TCP IPv4+ socket
def set_info(port):
    global s
    global s_ip
    ip = "0.0.0.0"  # socket.gethostbyname(socket.gethostname())
    s_ip = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(s_ip)
    wait_for_connection()


# Vent på at ein klient skal kople til på satt ip og port, returner 'Connected' tilkopling og klient ip på tilkopling
def wait_for_connection():
    print('Listening for connections on:\n  IP:', s_ip[0], ' Port:', s_ip[1])
    global connection
    global client_ip
    s.listen(1)
    while True:
        try:
            connection, client_ip = s.accept()
            print('Connected to IP:{} Port:{} '.format(client_ip[0], client_ip[1]))
            return
        except Exception:
            return
        finally:
            receive()


# Send ein beskjed til klienten. Bruk pickle til og enkelt sende variablar
def send_message(message):
    msg = pickle.dumps(message)
    while True:
        try:
            connection.sendall(msg)
            break
        except OSError:
            break


# Vent på ein melding frå klienten. Decode meldingen med pickle og returner meldingen
def receive():
    data = None
    print("waiting for data..")
    while True:
        try:
            data = connection.recv(1024)
        except socket.error as e:
            print('disconnected')

        finally:
            if data:
                coordinates = str(data.decode('utf-8'))
                k = coordinates.rfind(";") + 2
                coordinates = coordinates[k:]

                # dump, height, width = str(data.decode('utf-8')).split(", ")
                x, y = coordinates.split(", ")
                print("x: " + x + "\ty: " + y)
                move_mouse(int(x), int(y))


# Stop tilkoplinga
def close_connection():
    s.close()


def click(command):
    if command == "right":
        pyautogui.rightClick()
    if command == "left":
        pyautogui.click()
    if command == "double":
        pyautogui.doubleClick()


def move_mouse(x, y):
    pyautogui.moveRel(x, y, duration=0.1)

# while True:
# #     try:
# #         port = input('What port do you want to use?\n')
# #         port = int(port)
# #         if 10000 <= port <= 60000:
# #             break
# #         else:
# #             print('Please type in a number between 2000 and 10000\n')
# #     except ValueError:
# #         print('Please type in a number\n')

port = 22222

set_info(port)
