from .entities.Libro import Libro
import requests
import json
from flask import jsonify, render_template


class ModeloLibro():

    @classmethod
    def ConsultarLibros(self, db):
        data = []
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Libros")
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
            cursor.execute("SELECT * FROM Libros WHERE id_libro = %s",(id_libro))
            conn.close()
            libro = cursor.fetchone()
            print(libro)
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
    def unLibroDic(self, db, id_libro):
        data = []
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Libros WHERE id_libro = %s", (id_libro))
            conn.close()
            libro = cursor.fetchone()
            libro_obj = Libro(id_libro=id_libro, nombre=None, editorial=None, autor=None, stock=None, estatus=None,
                              precio=None, img_ruta=None)

            return libro
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False

    @classmethod
    def LibrosApi(self):
        url = "https://yg0isxnwaf.execute-api.us-east-1.amazonaws.com/libros/libros"

        # Tu API key
        api_key = "PCWtiB5khP60sa9X1jd2l4kFAQXMyC1E2SiiSHZV"

        # Cabeceras con la API key
        headers = {
            "x-api-key": api_key
        }
        response = requests.get(url,headers=headers)
        print(response)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            #body_json = json.loads(data['body'])
        return data

    @classmethod
    def descontarStock(self, unidades,id ):
        url = "https://yg0isxnwaf.execute-api.us-east-1.amazonaws.com/libros/libros"
        # Tu API key
        api_key = "PCWtiB5khP60sa9X1jd2l4kFAQXMyC1E2SiiSHZV"

        # Cabeceras con la API key
        headers = {
            "x-api-key": api_key
        }
        params = {
            "id": str(id),
            "unidades": unidades
        }
        print(params)
        response = requests.patch(url,headers=headers, json=params )

        data = response.json() if response.status_code == 200 else None
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
        return data


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

    @classmethod
    def insertarLibro(self, db, libro):
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Libros (id_libro, nombre, editorial, autor, stock, estatus,precio, img_ruta) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                (libro.id_libro,libro.nombre,libro.editorial, libro.autor,libro.stock,libro.estatus,libro.precio,libro.img_ruta))
            conn.commit()
            datosUsuario = cursor.fetchone()
            conn.close()
            if cursor.rowcount > 0:
                print("Registro insertado")
                return True
            else:
                print("No se encontraron registros para actualizar.")
                return False
        except Exception as ex:
            print("Error en la consulta sql: ", ex)
            return False

    @classmethod
    def Guardar_calificacion(self, db, rankings):
        try:
            if not rankings:
                print("Error: El objeto rankings es None")
                return {'error': 'El objeto rankings es None'}
            try:
                print("🔹 Intentando conectar a la base de datos...")
                conn = db.connect()
                print("✅ Conexión exitosa")
                cursor = conn.cursor()
            except Exception as e:
                print(f"❌ Error al conectar a la base de datos: {str(e)}")
                return jsonify({'error': f'Error al conectar a la base de datos: {str(e)}'}), 500

            conn = db.connect()
            cursor = conn.cursor()
            id_usuario = rankings.id_usuario
            id_libro = rankings.id_libro
            ranking = rankings.ranking


            cursor.execute(
                "SELECT ranking, cantidad_calificaciones, suma_calificaciones FROM Ranking WHERE id_usuario = %s AND id_libro = %s",
                (id_usuario, id_libro)
            )
            calificacion_existente = cursor.fetchone()

            if calificacion_existente:
                nueva_suma_calificaciones = calificacion_existente[2] + ranking
                nueva_cantidad_calificaciones = calificacion_existente[1] + 1
                cursor.execute(
                    "UPDATE Ranking SET ranking = %s, cantidad_calificaciones = %s, suma_calificaciones = %s WHERE id_usuario = %s AND id_libro = %s",
                    (ranking, nueva_cantidad_calificaciones, nueva_suma_calificaciones, id_usuario, id_libro)
                )
                print("CALIFICACION EXISTENTE 3")
            else:
                cursor.execute(
                    "INSERT INTO Ranking (id_usuario, id_libro, ranking, cantidad_calificaciones, suma_calificaciones) VALUES (%s, %s, %s, %s, %s)",
                    (id_usuario, id_libro, ranking, 1, ranking)
                )

            conn.commit()
            cursor.execute(
                "SELECT suma_calificaciones, cantidad_calificaciones FROM Ranking WHERE id_libro = %s",
                (id_libro,)
            )
            resultado = cursor.fetchone()

            if resultado:
                suma_calificaciones = resultado[0]
                cantidad_calificaciones = resultado[1]
                if cantidad_calificaciones > 0:
                    promedio = suma_calificaciones / cantidad_calificaciones
                    data = {'promedio': promedio,
                            'mensaje': 'Calificación guardada exitosamente y promedio actualizado.'}
                else:
                    data = {'mensaje': 'No hay calificaciones para este libro.'}
            else:
                data = {'mensaje': 'No se encontró el libro.'}
            conn.close()
            print(data)
            return jsonify(data)

        except Exception as e:
            return jsonify({'error': str(e)})

    def calcular_promedio(self,db, id_libro):
        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(ranking), COUNT(*) FROM Ranking WHERE id_libro = %s", (id_libro,))
        suma_calificaciones, cantidad_calificaciones = cursor.fetchone()

        if cantidad_calificaciones > 0:
            promedio = suma_calificaciones / cantidad_calificaciones
            promedio = int(promedio)
            return promedio
        else:
            promedio = 0
            return promedio

        conn.commit()
        conn.close()

    @classmethod
    def Verifica_calificacion(self, db, rankings):
        conn = db.connect()
        cursor = conn.cursor()
        id_usuario = rankings.id_usuario
        id_libro = rankings.id_libro
        cursor.execute("SELECT ranking from Ranking where id_usuario = %s AND id_libro = %s", (id_usuario, id_libro))
        la_puntuacion = cursor.fetchone()
        print("LA PUNTUACIÓN:",la_puntuacion)
        if la_puntuacion:
            try:
                return int(la_puntuacion[0])
            except ValueError:
                return None
        else:
            return None

    def verificarExistencias(self, db , id_libro, unidades):
        print(id_libro, unidades)
        conn = db.connect()
        cursor = conn.cursor()
        query = """
            SELECT CASE 
                WHEN stock >= %s THEN 1
                ELSE 0
            END AS es_posible
            FROM Libros
            WHERE id_libro = %s;
            """

        cursor.execute(query, (unidades, str(id_libro)))
        resultado = cursor.fetchone()

        conn.close()

        # Retornar True o False dependiendo del resultado
        if resultado:
            return resultado[0] == 1
        else:
            # Producto no encontrado
            return False