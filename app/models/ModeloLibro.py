from .entities.Libro import Libro
import requests
import json

class ModeloLibro():

    @classmethod
    def ConsultarLibros(self, db):
        data = []
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libros")
            conn.close()
            libros = cursor.fetchall()
            #print(libros)
            for libro in libros:
                if libros != None:
                    libro_obj = Libro(id_libro=None,nombre=None, editorial=None, autor=None, stock=None, estatus=None, precio=None, img_ruta=None)
                    libro_obj.id_libro = libro[0]
                    libro_obj.nombre = libro[1]
                    libro_obj.editorial = libro[2]
                    libro_obj.autor = libro[3]
                    libro_obj.stock = libro[4]
                    libro_obj.estatus = libro[5]
                    libro_obj.precio = libro[6]
                    libro_obj.img_ruta = libro[7]
                    data.append(libro)
            return data
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False

    @classmethod
    def unLibro(self, db, id_libro):
        data = []
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Libros where id_libro = {}".format(id_libro))
            conn.close()
            libro = cursor.fetchone()
            libro_obj = Libro(id_libro=id_libro, nombre=None, editorial=None, autor=None, stock=None, estatus=None,
                              precio=None, img_ruta=None)
            if libro != None:
                    libro_obj.nombre = libro[1]
                    libro_obj.editorial = libro[2]
                    libro_obj.autor = libro[3]
                    libro_obj.stock = libro[4]
                    libro_obj.estatus = libro[5]
                    libro_obj.precio = libro[6]
                    libro_obj.img_ruta = libro[7]
            return libro_obj
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False

    @classmethod
    def LibrosApi(self):
        url = "https://v7lo3sw1rk.execute-api.us-east-1.amazonaws.com/libreria_etapa"
        response = requests.get(url)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            body_json = json.loads(data['body'])
        return body_json

    @classmethod
    def Actualizar_Libro(cls, db, libro):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            print(libro.id_libro)
            cursor.execute(
                'UPDATE Libros SET nombre = %s, editorial = %s, autor = %s, stock = %s, estatus = %s, precio =%s WHERE id_libro = %s',
                (libro.nombre,libro.editorial, libro.autor, libro.stock, libro.estatus, libro.precio,libro.id_libro))
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
            print("Error en la consulta sql: ", ex)
            return False

    @classmethod
    def eliminarLibro(self,db, id):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM Libros WHERE id_libro = %s',
                (id))
            conn.commit()
            datosUsuario = cursor.fetchone()
            conn.close()
            if cursor.rowcount > 0:
                print("Registro eliminado")
                return True
            else:
                print("No se encontraron registros para actualizar.")
                return False
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False


