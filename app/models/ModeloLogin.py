from cryptography.fernet import Fernet
import bcrypt

from .entities.Login import Login

class ModeloLogin():

    @classmethod
    def ConsultarLogin(self, db, correo0, contrasena0):
        data = {}
        login = Login(id_login=None,correo=Login.desencriptar(correo0),contrasena=contrasena0,privilegio=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.callproc('VerificarUsuario',[login.correo,login.contrasena])
            conn.close()
            usuario = cursor.fetchone()
            print(usuario)
            if usuario != None:
                login.id_login=usuario[0]
                login.correo=usuario[1]
                login.contrasena=usuario[2]
                login.privilegio=usuario[3]
                return login
            else:
                return login
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False