import hashlib

def hash_gen(password: str):
    hasher = hashlib.sha256()
    password = password.encode("utf-8")
    hasher.update(password)
    new_password = hasher.hexdigest()
    return new_password

def hash_verify(passwd_attempt: str, passwd: str):
    hasher = hashlib.sha256()
    passwd_attempt = passwd_attempt.encode("utf-8")
    hasher.update(passwd_attempt)
    hashed_passwd = hasher.hexdigest()
    if passwd == hashed_passwd:
        return True
    return False