import hashlib

from Cryptodome.Hash import SHA256
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import keys
import socket
import json
import os
import config
from dtsp import *
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
# Конфигурирование порта и хоста из конфига
port = config.PORT
host = ''

# Создание сокета, связывание сокета с портом и адресом хоста
s = socket.socket()
s.bind((host, port))
s.listen(5)
# Создание переменной для json
file = os.getcwd() + '/keys.json'
signfile = os.getcwd() + '/signature.pem'
keyfile = os.getcwd() + '/key.pem'

def send_signature(signfile, conn):
    f = open(signfile, 'rb')
    l = f.read(1024)
    # Отправка данных
    while (l):
        conn.send(l)
        l = f.read(1024)
    f.close()

#write data in .pem file
def write_pem(content, file):
    with open(file, 'wb') as f:
        f.write(content)

def get_signature_and_key():
    key, signature = sign_file(file)
    write_pem(signature, signfile)
    write_pem(key, keyfile)
    print('Sign pem files...')

def main():
    print(f'Server listen specified port')
    # Запускаем наш слушающий сервер по порту, указанному в конфиге
    while True:
        conn, addr = s.accept()
        if conn:

            # Инициализация работы с БД на сервере
            engine = create_engine('sqlite:///Project_BD2.db')
            Session = sessionmaker(bind=engine)
            session = Session()
            Key = session.query(keys).all()
            arr_data = []
            with open(file, 'w') as f:
                for kk in Key:
                    arr_data.append(
                        {"Akey": kk.Akey,
                        "Cname": kk.Cname,
                        "Edate": kk.Edate,
                        "Ktype": kk.Ktype,
                         })
                f.write(json.dumps({"data": arr_data}, indent=4))

        # Чтение  файла
        get_signature_and_key()

        f = open(file,'rb')
        l = f.read(1024)

        # Отправка данных
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()
        print(f'Keys sended to {addr}')
        # Закрываем коннект
        conn.close()

if __name__ == "__main__":
    main()
