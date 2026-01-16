import socket
import tkinter as tk
from threading import Thread
from datetime import datetime
import os

SERVER_HOST = '194.67.206.24'  # Публичный IP хоста
SERVER_PORT = 5002
NAME = input("Твоё имя: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))
client.send(NAME.encode())


if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)


root = tk.Tk()
root.title("Чат - Клиент")
messages = tk.Text(root, height=20, width=60)
messages.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)
entry.focus()
entry.bind('<Return>', lambda e: send_msg())

def send_msg():
    msg = entry.get()
    if msg:
        client.send(msg.encode())
        entry.delete(0, tk.END)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            messages.insert(tk.END, msg + "\n")
            messages.see(tk.END)
        except:
            root.after(0, root.quit)
            break

Thread(target=receive, daemon=True).start()
root.protocol("WM_DELETE_WINDOW", lambda: client.close() or root.quit())
root.mainloop()

