from cryptography.fernet import Fernet
import bcrypt

from .entities.Login import Login

class ModeloLogin():

    @classmethod
    def ConsultarLogin(cls, db, correo0, contrasena0):
        data = {}
        login = Login(id_login=None,correo=Login.desencriptar(correo0),contrasena=contrasena0,privilegio=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.callproc('VerificarUsuario',[login.correo,login.contrasena])
            conn.close()
            usuario = cursor.fetchone()
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
            return login

    @classmethod
    def Consultar_un_Login(cls,db,id_login0):
        login = Login(id_login=id_login0, correo=None, contrasena=None, privilegio=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Logins WHERE (id_login = {})'.format(id_login0))
            datosUsuario = cursor.fetchone()
            conn.close()
            login.id_login = datosUsuario[0]
            login.correo = datosUsuario[1]
            login.contrasena = datosUsuario[2]
            return login
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return login
    
    @classmethod
    def Actualizar_un_Login(cls, db, login):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('UPDATE Logins SET correo = %s, contrasena = %s  WHERE id_login = %s',(login.correo, login.contrasena, login.id_login))
            conn.commit()
            datosUsuario = cursor.fetchone()
            conn.close()
            if cursor.rowcount > 0:
                print("Actualización exitosa.")
                return True
            else:
                print("No se encontraron registros para actualizar.")
                return False
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return False