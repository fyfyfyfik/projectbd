# https://ru.wikibooks.org/wiki/SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import keys
import socket
import json
import os
import config

port = config.PORT
host = config.HOST

s = socket.socket()
s.bind((host, port))
s.listen(2)
file = os.getcwd() + '/keys.json'

def main():
    print(f'Server listen {port}')
    while True:
        conn, addr = s.accept()
        if conn:

            engine = create_engine('sqlite:///Project_DB2.db')
            Session = sessionmaker(bind=engine)
            session = Session()
            key = session.query(keys).all()
            arr_data = []
            with open(file, 'w') as f:
                for kk in key:
                    arr_data.append(
                        {"Akey": kk.Akey,
                        "Cname": kk.Cname,
                        "Edate": kk.Edate,
                        "Ktype": kk.Ktype,
                         })
                f.write(json.dumps({"data": arr_data}, indent=4))
        f = open(file,'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()
        print(f'Successfully sending to {addr}')
        conn.close()

if __name__ == "__main__":
    main()