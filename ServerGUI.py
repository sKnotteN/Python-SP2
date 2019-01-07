"""
Author: Kristian Saure Knotten
Student ID: 8284
E-mail: ksknotten@outlook.com
"""

from tkinter import *
import threading
import Server


class GUI(Tk):

    def __init__(self, ip):
        Tk.__init__(self)
        self.geometry("190x210")
        self.title("PC Control")
        # self.resizable(width=False, height=False)
        # Lag ein protokoll for vist brukaren kryssar ut vindauget
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.ip = "Server IP: " + ip

        self.port_frame = Frame(self).place(anchor=CENTER)

        self.ip_label = Label(self, text=self.ip).grid(row=0, pady=10, columnspan=2)

        self.port_label = Label(self, text="Port: ").grid(row=1, column=0, pady=10, padx=5)
        self.port_entry = Entry(self, width=5)
        self.port_entry.grid(row=1, column=1, pady=10, ipadx=1)
        self.port_entry.insert(END, "11111")

        self.info_message = StringVar()
        self.message_label = Label(self, textvariable=self.info_message, width=25).grid(row=2, columnspan=2, pady=10)

        self.start_btn = Button(self, text="Start", command=self.start_server)
        self.start_btn.grid(row=3, column=0, pady=10)
        self.stop_btn = Button(self, text="Stop", command=self.stop_server).grid(
            row=3, column=1, pady=10)

        self.server_message = StringVar()
        self.message_label = Label(self, textvariable=self.server_message, width=25).grid(row=4, columnspan=2, pady=10)

        # Gi serveren ein referanse til GUI
        Server.gui = self

    def start_server(self):
        print(self.port_entry.get())
        try:
            if self.port_entry.get() and 10000 <= int(self.port_entry.get()) <= 60000:
                self.server_message.set("Waiting for client")
                threading.Thread(target=self.connect).start()
            else:
                self.info_message.set('Use a port between 10000 and 60000')
        except ValueError:
            self.info_message.set("Please use only numbers")

    def connect(self):
        self.start_btn.config(state="disabled")
        message = Server.set_info(int(self.port_entry.get()))
        if message:
            self.server_message.set('Connected to ' + message[0])
            Server.receive()
        else:
            self.info_message.set('Not able to connect')

    def stop_server(self):
        try:
            Server.close_connection()
        except AttributeError:
            print('Start first')
            return

        self.start_btn.config(state="normal")
        self.server_message.set('Stopped listening')

    def close(self):
        self.destroy()

        try:
            self.stop_server()
        except TclError:
            print("tclerror")

        print("Closed")
        quit()
        return


GUI = GUI("0.0.0.0")
GUI.mainloop()
