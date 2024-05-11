from socket import *
from threading import Thread

# Connection Data
host = '127.0.0.1'
port = 7000

def init_network():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((host, port))
    turn =client.recv(1024).decode("utf-8")
    return turn,client