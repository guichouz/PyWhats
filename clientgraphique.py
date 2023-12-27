import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = 'localhost'
PORT = 55555

class Client:
    def __init__(self, host, port):
        # Initialisation du socket client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Configuration initiale de l'interface graphique
        msg = tkinter.Tk()
        msg.withdraw()

        # Demande du pseudonyme à l'utilisateur
        self.nickname = simpledialog.askstring("Pseudonyme", "Choisissez un pseudonyme", parent=msg)

        # Variables pour contrôler l'état de l'interface graphique et du client
        self.gui_done = False
        self.running = True

        # Démarrage des threads pour l'interface graphique et la réception des messages
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        # Configuration et création des éléments de l'interface graphique
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        # Création d'un tag pour styliser certains messages en rouge
        self.text_area.tag_config('red', foreground='red')

        self.msg_entry = tkinter.Entry(self.win, bg="white")
        self.msg_entry.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Envoyer", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        # Envoi des messages écrits par l'utilisateur
        message = f"{self.nickname}: {self.msg_entry.get()}"
        self.sock.send(message.encode('utf-8'))
        self.msg_entry.delete(0, tkinter.END)

    def stop(self):
        # Arrêt du client lorsque la fenêtre est fermée
        self.running = False
        self.win.destroy()
       
