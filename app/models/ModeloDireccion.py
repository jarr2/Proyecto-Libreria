from models.entities.Direccion import Direccion
from models.entities.Login import Login
from models.entities.Usuario import Usuario

class ModeloDireccion():

    @classmethod
    def Actualizar_Direccion(cls, db, usuario, direccion):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.callproc('ActualizarDireccionyUsuario',[usuario.id_usuario,
                                                           direccion.id_direccion,
                                                           usuario.nombre,
                                                           usuario.apellidos,
                                                           usuario.numero_telefonico,
                                                           direccion.calle,
                                                           direccion.num_interior,
                                                           direccion.num_exterior,
                                                           direccion.municipio,
                                                           direccion.colonia,
                                                           direccion.estado,
                                                           direccion.cp])
            conn.commit()
            dirNombre = cursor.fetchone()
            cursor.close()
            conn.close()
            print(dirNombre)
            return dirNombre
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False
        
    
    @classmethod
    def Consulta_Direccion(cls, db, id_direccion0):
        direccion = Direccion(id_direccion=id_direccion0, calle=None, estado=None, municipio=None, colonia=None, cp=None, num_interior=None, num_exterior=None)
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Direcciones WHERE (id_direccion = {})'.format(direccion.id_direccion))
            dirNombre = cursor.fetchone()
            conn.close()
            direccion.id_direccion = dirNombre[0]
            direccion.calle = dirNombre[1]
            direccion.estado = dirNombre[2]
            direccion.municipio = dirNombre[3]
            direccion.colonia = dirNombre[4]
            direccion.cp = dirNombre[5]
            direccion.num_interior = dirNombre[6]
            direccion.num_exterior = dirNombre[7]
            return direccion
        except Exception as ex:
            print("Error en la consulta sql: ",ex)
            return direccion
    
