import os

from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15



def read_pem(file, b=False):
    if not b:
        with open(file, "r") as f:
            return f.read()
    else:
        with open(file, "rb") as f:
            return f.read()

def sign_file(file):
    # Генерируем новый ключ
    private_key = RSA.generate(1024, os.urandom)
    # Получаем хэш файла
    hash = SHA256.new()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)

    # Подписываем хэш
    signature = pkcs1_15.new(private_key).sign(hash)

    # Получаем открытый ключ из закрытого
    pub_key = private_key.publickey().exportKey(format='PEM')
    return pub_key, signature



def check_sign(file_name, k_pem, s_pem):

    pubkey = RSA.importKey(read_pem(k_pem))
    signature = read_pem(s_pem, True)

    hash = SHA256.new()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)

    # Переменная для проверки подписи
    check_sign = False
    try:
        pkcs1_15.new(pubkey).verify(hash, signature)
        check_sign = True
        return check_sign
    except Exception as e:
        print(e)
        return check_sign
