"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

# https://automatetheboringstuff.com/chapter18/
# https://www.youtube.com/watch?v=2BXr9U6ZL8Y


# Importer dei offentlige bibloteka
import socket
import threading
from queue import Queue
from pynput.mouse import Button, Controller


# Set nokre variablar som skal vere lett tilgjengelege
s = None
s_ip = None
connection = None
client_ip = None
threads = []
gui = None

# Lag ein kø variabel til trådar
command_queue = Queue()

# Lag ein kontroller til musa
mouse = Controller()


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

    # Start opp trådar og gjer dei klar for input frå klienten
    threads = []
    for i in range(5):
        t = threading.Thread(target=handle_commands)
        t.start()
        threads.append(t)

    print("waiting for data..")
    while True:
        try:
            data = connection.recv(1024)

        # Om det dukkar opp nåken problemer med tilkoplinga så lukk sockets
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
            # Put kommandoen i tråd køa
            command_queue.put(data)

        else:
            # Lukk tilkoplinga og opn opp for ei ny tilkopling
            print("Disconnected")
            close_connection()
            if gui:
                gui.server_message.set("Client disconnected")
            set_info(s_ip[1])
            receive()
            break


# Stop tilkoplinga
def close_connection():
    # Lukk å clear trådane som ligg i kø
    while not command_queue.empty():
        command_queue.get()

    # with command_queue.mutex:
    #     command_queue.queue.clear()
    threads.clear()

    # Sjekk om der er noken som er tilkopla
    try:
        connection.close()

    except AttributeError:
        print('No connection found')

    s.close()
    print("Connection dropped")


# Handterer dei 5 trådane som vart laga
def handle_commands():
    while True:
        cmd = command_queue.get()
        pass_command(cmd)
        command_queue.task_done()


# Handterer kommandoane som kjem frå klienten
def pass_command(data):
    try:
        command = str(data.decode('utf-8'))
    except ValueError:
        print("Command is not valid")
        return

    # Sjekk om klienten prøvar og flytte på musa
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
            mouse.scroll(0, x)


# Utfør dei forskjellige kommandoane
def click(command):
    print(command)
    if command.endswith("rightdown"):
        mouse.press(Button.right)
    elif command.endswith("rightup"):
        mouse.release(Button.right)

    elif command.endswith("leftdown"):
        mouse.press(Button.left)
    elif command.endswith("leftup"):
        mouse.release(Button.left)

    # Om ikkje høgre klikk eller venstre klikk så er det scroll kommando
    else:
        return True


# Beveg musa til x og y posisjon
def move_mouse(x, y):
    mouse.move(x, y)


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
