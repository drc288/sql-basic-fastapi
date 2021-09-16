from cryptography.fernet import Fernet as _fm

def enc(msg: str):
    key = _fm.generate_key()
    f = _fm(key)

    return f.encrypt(msg.encode("utf-8"))

def dec(hash: str):
    return _fm.decrypt(hash).decode()
