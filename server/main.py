import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import keys
import socket
import json
import os
import config
import time
import itertools
import threading
import sys

from Cryptodome.Signature import pkcs1_15
import Cryptodome.Cipher.AES as AES
from Cryptodome.PublicKey import RSA

# Конфигурирование порта и хоста из конфига
port = 60000
host = 'localhost'

# Создание сокета, связывание сокета с портом и адресом хоста
s = socket.socket()
s.bind((host, port))
s.listen(5)
# Создание переменной для json
file = os.getcwd() + '/keys.json'


def main():
    print(f'Server listen specified port')
    # Запускаем наш слушающий сервер по порту, указанному в конфиге

    while True:
        conn, addr = s.accept()
        gethash = 0
        if conn:
            getpbk = conn.recv(2048)
            # публичный ключ сервера
            server_public_key = RSA.importKey(getpbk)
            if getpbk != "":
                conn.send("YES")
                gethash = conn.recv(1024)
                print("\n-----HASH OF PUBLIC KEY----- \n" + gethash)

            # хэшируем публичный ключ на стороне сервера для вадлидации полученного от клиента
            hash_object = hashlib.sha1(getpbk)
            hex_digest = hash_object.hexdigest()

            if hex_digest == gethash:
                # creating session key
                key_128 = os.urandom(16)
                # encrypt CTR MODE session key
                en = AES.new(key_128, AES.MODE_CTR, counter=lambda: key_128)
                encrypto = en.encrypt(key_128)
                # hashing sha1
                en_object = hashlib.sha1(encrypto)
                en_digest = en_object.hexdigest()

                print("\n-----SESSION KEY-----\n" + en_digest)

                # encrypting session key and public key
                E = server_public_key.encrypt(encrypto, 16)
                print("\n-----ENCRYPTED PUBLIC KEY AND SESSION KEY-----")
                print("\n-----HANDSHAKE COMPLETE-----")

            else:
                print("\n-----PUBLIC KEY HASH DOESNOT MATCH-----\n")
                continue
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
        # Чтение файла
        f = open(file, 'rb')
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
