import socket


def cts(filename: str) -> None:
    """Отправление файла на сервер"""
    with open(filename, 'rb') as f:
        a = f.read()
    sock.send(a)


def ctc() -> None:
    """Принятие файла с сервера"""
    filename = sock.recv(1024).decode()
    print(filename)
    a = b''
    while True:
        data = sock.recv(1024)
        a += data
        if not data:
            break
    with open(filename, 'wb') as f:
        f.write(a)


HOST = 'localhost'
PORT = 1025
print("Для помощи напишите help.")
while True:
    request = input('>')

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(request.encode())
    if request[:4] == 'cts ':
        cts(request[4:])

    response = sock.recv(1024).decode()
    if response == 'file':
        ctc()
    print(response)
    sock.close()
    if response == 'exit':
        print("Отключение от сервера.")
        break
