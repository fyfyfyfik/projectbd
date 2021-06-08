import hashlib
import os
import ipaddress
import form
import sys
import socket  # Импорт модуля сокета
import json
from dtsp import *
from random import choice
from PyQt5 import QtWidgets, uic
import config
from Cryptodome import Random
from Cryptodome.PublicKey import RSA


s = socket.socket()  # Создание объекта сокета
# Получение порта и айпи из переменных окружения
port = config.PORT
host = socket.gethostname()

# Переменная для файла json
file = os.getcwd() + '/keys.json'
final_sign =  os.getcwd() + '/final_signature.pem'
final_key =  os.getcwd() + '/final_key.pem'
#Calculate hash of recieved file at clients side
def find_hash():
    hash = hashlib.sha256(file)
    # Чтение и получение хэша файла
    f = open(file, 'rb')
    for chunk in iter(lambda: f.read(4096), b""):
        hash.update(chunk)
    return hash

# Функция для проверки валидности айпи
def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True


def put_data(s, final_file):
    with open(final_file, 'wb') as f:
        while True:
            print('receiving data...')
            data = s.recv(1024)
            if not data:
                break
            # write data to a file
            f.write(data)

# Получение контента по именам из файла, например get_content('Akey')
def get_content(name):
    name_arr = []
    with open(file, 'r') as f:
        data = json.loads(f.read())
    arr = data['data']
    for el in arr:
        name_arr.append(el[name])
    return name_arr


# Подключение к серверу и скачивание нового файла json
def update_base(ip):
    s.connect((ip, port))
    put_data(s,final_sign)
    put_data(s,final_key)
    with open(file, 'wb') as f:
            while True:
                print('receiving data...')
                data = s.recv(1024)
                if not data:
                    break
                # write data to a file
                f.write(data)
    f.close()
    try:
        check_sign(file,final_key,final_sign)
        print('Successfully downloaded file')
    except(ValueError,TypeError):
        print('The signature isn\'t valid')
    s.close()
    print('connection closed with 185.104.113.203')


# Окно приложения
class App(QtWidgets.QMainWindow, form.Ui_MainWindow):
    # Инициализация
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)

        # Коннектим кнопки к нужным функциям
        self.pushButton.clicked.connect(self.update_key)
        self.pushButton_6.clicked.connect(self.update_keygen)

    # Замапленные кнопки выполняют функции
    def update_key(self):
        try:
            arr = get_content('Akey')
            self.textBrowser_4.setText(choice(arr))
            arr = get_content('Cname')
            self.textBrowser_2.setText(choice(arr))
            arr = get_content('Edate')
            self.textBrowser.setText(choice(arr))
            arr = get_content('Ktype')
            self.textBrowser_3.setText(choice(arr))
        except Exception as e:
            # если ошибка то вылетает окошко с ошибкой
            errorWin = QtWidgets.QErrorMessage(self)
            errorWin.showMessage(f'Ошибка: \n{e}')

    # Кнопка обновления локальной базы
    def update_keygen(self):
        # Спрашиваем у пользователя IP
        ip, yes = QtWidgets.QInputDialog.getText(self, 'Вход', 'Введите ip key-сервера:')
        if yes and valid_ip(ip) or ip == 'localhost':
            try:
                update_base(ip)
            except Exception as e:
                errorWin = QtWidgets.QErrorMessage(self)
                errorWin.showMessage(f'Ошибка: \n{e}')

# MAIN
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    app.exec_()
