from passlib.context import CryptContext


class Security():

    def verify_password(self, password: str, hash_password: str) -> bool:
        crypto = CryptContext(schemes=['bcrypt'], deprecated='auto')

        return crypto.verify(password, hash_password)


    def hash_generator(self, password: str) -> str:
        crypto = CryptContext(schemes=['bcrypt'], deprecated='auto')

        return crypto.hash(password)
    
security = Security()
