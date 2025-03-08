from models.entities.Usuario import Usuario
from flask import jsonify
import json
class ModeloUsuario():
    
    @classmethod
    def Consulta_Usuario(cls, db, id_login):
        usuario = Usuario(id_usuario=None, id_direccion=None, id_login=None, nombre=None, apellidos=None, numero_telefonico=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Usuarios WHERE (id_login = {})'.format(id_login))
            datosUsuario = cursor.fetchone()
            conn.close()
            usuario.id_usuario = datosUsuario[0]
            usuario.id_direccion = datosUsuario[1]
            usuario.id_login = datosUsuario[2]
            usuario.nombre = datosUsuario[3]
            usuario.apellidos = datosUsuario[4]
            usuario.numero_telefonico = datosUsuario[5]
            return usuario
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return usuario
    
    @classmethod
    def Consultar_Nombre(cls, db, id_login):
        nombre = ''
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT nombre FROM Usuarios WHERE (id_login = {})'.format(id_login))
            datosUsuario = cursor.fetchone()
            conn.close()
            nombre = datosUsuario[0]
            return nombre
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return nombre
    
    @classmethod
    def Consultar_Usuarios(cls, db):
        usuarios = ''
        data = {}
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("""
                            SELECT
                                Usuarios.id_login,
                                Usuarios.id_usuario,
                                Usuarios.id_direccion,
                                Usuarios.nombre,
                                Usuarios.apellidos,
                                Logins.correo
                            FROM 
                                Usuarios
                            INNER JOIN 
                                Logins
                            ON 
                                Usuarios.id_login = Logins.id_login
                            WHERE 
                                Logins.privilegio = 'user';
                            """)
            usuarios = cursor.fetchall()
            conn.close()
            data={'usuarios': usuarios}
            print(data)
            return data
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return data
    
    @classmethod
    def Actualizar_un_Usuario(cls, db, usuario):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('UPDATE Usuarios SET nombre = %s, apellidos = %s, numero_telefonico = %s WHERE id_login = %s', (usuario.nombre, usuario.apellidos, usuario.numero_telefonico, usuario.id_login))
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