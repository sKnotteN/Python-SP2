"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# https://automatetheboringstuff.com/chapter18/
# https://www.youtube.com/watch?v=2BXr9U6ZL8Y


# Importer dei offentlige bibloteka
import socket
import pyautogui
import threading
from queue import Queue


# Set nokre variablar som skal vere lett tilgjengelege
s = None
s_ip = None
connection = None
client_ip = None
screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False
threads = []

command_queue = Queue()


# Lagrer informasjonen som skal bli brukt i variabler. Lag ein TCP IPv4+ socket
def set_info(port):
    global s
    global s_ip
    ip = "0.0.0.0"
    s_ip = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(s_ip)
    return wait_for_connection()


# Vent på at ein klient skal kople til på satt ip og port, returner 'Connected' tilkopling og klient ip på tilkopling
def wait_for_connection():
    print('Listening for connections on:\n  IP:', s_ip[0], ' Port:', s_ip[1])
    global connection
    global client_ip
    s.listen(1)
    try:
        connection, client_ip = s.accept()
        return client_ip
    except Exception:
        return None
    # finally:
    #     receive()


# Send ein beskjed til klienten.
def send_message(message):
    while True:
        try:
            connection.sendall(message)
            break
        except OSError:
            break


# Vent på ein melding frå klienten.
def receive():
    global threads
    data = None

    threads = []
    for i in range(5):
        t = threading.Thread(target=handle_commands)
        t.start()
        threads.append(t)

    print(threads)

    print("waiting for data..")
    while True:
        try:
            data = connection.recv(1024)

        except socket.error:
            print('Socket error')
            close_connection()
            break
        except KeyboardInterrupt:
            print("Halt by user")
            close_connection()
            break
        except SystemExit:
            close_connection()
            break

        if data:
            print("Received data", data)
            # Start en tråd som handterer bevegelsar og klikk for og få fleire oppdateringar i sekundet
            """
            t = threading.Thread(target=pass_command, args=(data,))
            t.setDaemon(True)
            t.start()
            """
            command_queue.put(data)
            # pass_command(data)
        else:
            print("No data received")
            # Lukk tilkoplinga og opn opp for ei ny tilkopling
            print("Disconnected")
            close_connection()
            set_info(s_ip[1])
            receive()
            break


# Stop tilkoplinga
def close_connection():
    with command_queue.mutex:
        command_queue.queue.clear()
    threads.clear()

    connection.close()
    # s.shutdown(socket.SHUT_WR)
    s.close()
    print("Connection dropped")

def handle_commands():
    while True:
        cmd = command_queue.get()
        pass_command(cmd)
        command_queue.task_done()

# Ikkje optimal
def pass_command(data):
    try:
        command = str(data.decode('utf-8'))
    except ValueError:
        print("Command is not valid")
        return

    try:
        k = command.rfind(";") + 2
        coordinates = command[k:]

        x, y = coordinates.split(", ")

        move_mouse(int(x), int(y))
        print("x: " + x + "\ty: " + y)

    except ValueError:
        # Om Click funksjonen returnerer True er det ein scroll kommando
        if click(command):
            # Oppsett slik at x her egentlig blir y
            pyautogui.scroll(int(x))


# Utfør dei forskjellige kommandoane
def click(command):
    print(command)
    if command.endswith("rightdown"):
        pyautogui.mouseDown(button='right')
    elif command.endswith("rightup"):
        pyautogui.mouseUp(button='right')

    elif command.endswith("leftdown"):
        pyautogui.mouseDown(button='left')
    elif command.endswith("leftup"):
        pyautogui.mouseUp(button='left')

    # Om ikkje høgre klikk eller venstre klikk så er det scroll kommando
    else:
        return True


# Beveg musa til x og y posisjon
def move_mouse(x, y):
    pyautogui.moveRel(x, y, 0.1, pyautogui.easeInQuad)


# Spør brukaren kass port han vil høyre på
def ask_port():
    global port
    while True:
        try:
            port = input('What port do you want to use?\n')
            port = int(port)
            if 10000 <= port <= 60000:
                break
            else:
                print('Please type in a number between 2000 and 10000\n')
        except ValueError:
            print('Please type in a number\n')


# port = 22222
# # ask_port()
# set_info(port)
#
# input("press")