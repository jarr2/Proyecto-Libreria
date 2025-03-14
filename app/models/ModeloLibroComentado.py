from models.entities.Libro_Comentado import Libro_Comentado
class ModeloLibroComentado():

    @classmethod
    def comentar(cls,db, Libro_Comentado):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Libro_Comentado (id_libro, id_usuario, comentario, bandera) VALUES(%s,%s,%s,%s)',
                (Libro_Comentado.id_libro, Libro_Comentado.id_usuario,Libro_Comentado.comentario,Libro_Comentado.bandera))
            conn.commit()
            conn.close()
            if cursor.rowcount > 0:
                print("Registro insertado")
                return True
            else:
                print("Algo falló yo no sé tú si?")
                return False
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
        return False

    @classmethod
    def ConsultarLibroComentado(self, db, id_libro):
        data = []
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Libro_Comentado as lc ,Usuarios as usr WHERE lc.id_libro = %s and (lc.id_usuario= usr.id_usuario) ", (id_libro,))
            conn.close()
            libros = cursor.fetchall()
            # print(libros)
            for libro in libros:
                if libros != None:
                    libro_obj = Libro_Comentado(id_comentario=None, id_libro=None, id_usuario=None,id_login=None, id_direccion=None,nombre=None,apellidos=None, numero_telefonico=None, comentario=None, bandera=None)
                    libro_obj.id_comentario = libro[0]
                    libro_obj.id_usuario = libro[1]
                    libro_obj.id_libro = libro[2]
                    libro_obj.comentario = libro[3]
                    libro_obj.bandera = libro[4]
                    libro_obj.id_direccion = libro[6]
                    libro_obj.id_login = libro[7]
                    libro_obj.nombre = libro[8]
                    libro_obj.apellidos = libro[9]
                    libro_obj.numero_telefonico = libro[10]
                    data.append(libro)
            return data
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False