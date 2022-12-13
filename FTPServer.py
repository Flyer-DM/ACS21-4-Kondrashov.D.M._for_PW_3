import socket
import os


PORT = 1025
os.chdir('users')
curr_dir = os.getcwd()


def help() -> str:
    """Сообщение доступных команд"""
    message = '''pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
exit - отключение клиента
mkdir <directory name> - создание директории
rmdir <directory name> - удаление директории и всего содержимого рекурсивно
rm <filename> - удаление файла
rename <filename> <new filename> - переименование файла
cts <filename> - копирование файла на сервер
ctc <filename> - копирование файла на клиент'''
    return message


def cat(req: str) -> str:
    """Чтение содержимого файла"""
    filename = req[4:]
    try:
        filename = curr_dir + '/' + filename
        with open(filename) as f:
            return f.read()
    except OSError:
        return "Файл не найден"


def mkdir(req: str) -> str:
    """Создание директории"""
    dirname = req[6:]
    try:
        dirname = curr_dir + '/' + dirname
        os.mkdir(dirname)
        dirname = dirname.replace('/', '\\')
        return f"Папка {dirname} успешно создана."
    except OSError:
        return "This directory already exists"


def rmdir(req: str):
    """Удаление директории рекурсивно"""
    try:
        os.rmdir(curr_dir+'/'+req)
    except:
        os.chdir(curr_dir+'/'+req)
        for i in os.listdir(curr_dir+'/'+req):
            try:
                rmdir(req+'/'+i)
            except:
                os.remove(i)
        os.chdir(curr_dir+'/..')
        os.rmdir(curr_dir+'/'+req)


def rm(req: str):
    """Удаление файлов"""
    try:
        os.remove(curr_dir + '/' + req)
        return f"Файл {req} успешно удалён."
    except OSError:
        return "Файл для удаления не найден."


def rename(req: str):
    """Переименование файлов"""
    try:
        src = req[:req.find(' ')]
        dst = req[req.find(' ') + 1:]
        os.rename(src, dst)
        return f"Файл {src} переименован в {dst}."
    except OSError:
        return "Файл или директория не найдена."
    except:
        return "Непредвиденная ошибка в переименовании файла."


def cts(filename: str):
    """Получение файла от клиента"""
    a = b''
    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            break
        a += data
    with open(filename, 'wb') as f:
        f.write(a)
    return "Файл успешно получен."


def ctc(filename: str):
    """Отправка файла клиенту"""
    conn.send('file'.encode())
    conn.send(filename.encode())
    with open(filename, 'rb') as f:
        a = f.read()
    conn.send(a)
    return "Файл успешно отправлен"


def process(req):
    if req == 'exit':
        return 'exit'
    elif req == 'pwd':
        return curr_dir
    elif req == 'ls':
        return '\n'.join(os.listdir(curr_dir))
    elif req[:4] == 'cat ':
        return cat(req)
    elif req[:6] == 'mkdir ':
        return mkdir(req)
    elif req[:6] == 'rmdir ':
        return rmdir(req[6:])
    elif req[:3] == 'rm ':
        return rm(req[3:])
    elif req[:7] == 'rename ':
        return rename(req[7:])
    elif req[:4] == 'cts ':
        return cts(req[4:])
    elif req[:4] == 'ctc ':
        return ctc(req[4:])
    elif req == 'help':
        return help()
    else:
        return 'bad request'


sock = socket.socket()
sock.bind(('', PORT))

sock.listen()
while True:
    print("Сервер запущен.")
    conn, addr = sock.accept()
    conn.settimeout(1)

    request = conn.recv(1024).decode()
    print(request)
    response = process(request)
    conn.send(response.encode())

    conn.close()
