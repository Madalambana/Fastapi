from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt(password: str):
    return pwd_context.hash(password)

def compare(plain_password, encrypt):
    return pwd_context.verify(plain_password,encrypt)