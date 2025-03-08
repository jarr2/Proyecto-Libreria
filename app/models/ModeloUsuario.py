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
            if cursor.rowcount > 0 and cursor.rowcount <= 3:
                print("Actualización exitosa.")
                return True
            else:
                print("No se encontraron registros para actualizar.")
                return False
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return False
    
    @classmethod
    def Crear_un_Usuario(cls, db, login, usuario, direccion):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("""
                            INSERT INTO Direcciones (calle, estado, municipio, colonia, cp, num_exterior, num_interior)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """, (direccion.calle, direccion.estado, direccion.municipio, direccion.colonia, direccion.cp, direccion.num_exterior, direccion.num_interior))
            direccion.id_direccion = cursor.lastrowid
            cursor.execute("""
                            INSERT INTO Logins (correo, contrasena, privilegio)
                            VALUES (%s, %s, %s)
                            """, (login.correo, login.contrasena, login.privilegio))
            login.id_login = cursor.lastrowid
            cursor.execute("""
                            INSERT INTO Usuarios (id_direccion, id_login, nombre, apellidos, numero_telefonico)
                            VALUES (%s, %s, %s, %s, %s)
                             """, (direccion.id_direccion, login.id_login, usuario.nombre, usuario.apellidos, usuario.numero_telefonico))
            conn.commit()
            conn.close()
            if cursor.lastrowid:
                return True
            else:
                return False
        
        except Exception as ex:
            print('Error en la consulta sql:', ex)
            return False
    
    @classmethod
    def Eliminar_un_Usuario(cls, db, ids):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s",ids[1])
            filas_borradas_usuarios = cursor.rowcount
            cursor.execute("DELETE FROM Logins WHERE id_login = %s",ids[0])
            filas_borradas_logins = cursor.rowcount
            cursor.execute("DELETE FROM Direcciones WHERE id_direccion = %s",ids[2])
            filas_borradas_direcciones = cursor.rowcount
            conn.commit()
            if filas_borradas_usuarios > 0 or filas_borradas_logins > 0 or filas_borradas_direcciones > 0:
                print('registros eliminados correctamente')
                return True
            else:
                return False
        except db.conn.Error as err:
            conn.rollback()
            print(f'Error al eliminar registros: {err}','danger')
        finally:
            cursor.close()
            conn.close()
