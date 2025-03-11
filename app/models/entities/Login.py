from cryptography.fernet import Fernet
import bcrypt


class Login():

    def __init__(self, id, correo, contrasena, privilegio):
        self.id = id
        self.correo = correo
        self.contrasena = contrasena
        self.privilegio = privilegio

    @classmethod
    def encriptar(cls, dato):
        key = b'MBM6KtJWagJf3dbl02QBqB4mblalri2noHfM9dss6YI='
        fernet = Fernet(key)
        datoEnc = fernet.encrypt(dato.encode('utf-8'))
        return datoEnc

    @classmethod
    def desencriptar(cls,dato):
        key = b'MBM6KtJWagJf3dbl02QBqB4mblalri2noHfM9dss6YI='
        fernet = Fernet(key)
        datoDesenc = fernet.decrypt(dato).decode('utf-8')
        return datoDesenc
    
    @classmethod
    def encriptarContr(cls, dato):
        sal = b'$2b$12$Bj2s7PI42QkpqlbJtkAH/e'
        datoEnc = dato.encode('utf8')
        Contra = str(bcrypt.hashpw(datoEnc, sal))
        return Contra
    
    @classmethod
    def compararContr(cls, dato, hach):
        if bcrypt.checkpw(dato, hach):
            print("Que mirai vieja conchetumare")
            return True
        else:
            return False