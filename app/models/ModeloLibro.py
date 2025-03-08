from .entities.Libro import Libro

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
            cursor.execute("SELECT * FROM libros where id_libro = {}".format(id_libro))
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
