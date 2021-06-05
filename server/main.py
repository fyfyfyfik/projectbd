from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import keys
import socket
import json
import os
import config

# Конфигурирование порта и хоста из конфига
port = config.PORT
host = ''

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

        # Чтение файла
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