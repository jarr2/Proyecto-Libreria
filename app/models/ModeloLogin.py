from cryptography.fernet import Fernet
import bcrypt

from .entities.Login import Login
from .entities.Usuario import Usuario
from .entities.LoginUser import LoginUser

class ModeloLogin():

    @classmethod
    def ConsultarLogin(cls, db, correo0, contrasena0):
        data = {}
        login = Login(id=None,correo=Login.desencriptar(correo0),contrasena=contrasena0,privilegio=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.callproc('VerificarUsuario',[login.correo,login.contrasena])
            conn.close()
            usuario = cursor.fetchone()
            if usuario != None:
                login.id=usuario[0]
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
        login = Login(id=id_login0, correo=None, contrasena=None, privilegio=None)
        usuario = Usuario(id_usuario=None,id_direccion=None,id_login=None,nombre=None,apellidos=None,numero_telefonico=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("""SELECT 
                                Usuarios.id_usuario,
                                Usuarios.id_direccion,
                                Usuarios.nombre,
                                Logins.id_login,
                                Logins.correo,
                                Logins.privilegio
                            FROM 
                                Usuarios
                            JOIN 
                                Logins
                            ON 
                                Usuarios.id_login = Logins.id_login
                            WHERE 
                                Logins.id_login = %s """,(id_login0))
            datosUsuario = cursor.fetchone()
            conn.close()
            usuario.id_usuario = datosUsuario[0]
            usuario.id_direccion = datosUsuario[1]
            usuario.nombre = datosUsuario[2]
            login.id = datosUsuario[3]
            login.correo = datosUsuario[4]
            login.privilegio = datosUsuario[5]
            usuario_logueado = LoginUser(login, usuario)
            return usuario_logueado
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return login
    
    @classmethod
    def Actualizar_un_Login(cls, db, login):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('UPDATE Logins SET correo = %s, contrasena = %s  WHERE id_login = %s',(login.correo, login.contrasena, login.id))
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