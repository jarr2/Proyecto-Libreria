from.Usuario import Usuario

class Libro_Comentado(Usuario) :
        def __init__(self, id_comentario, id_usuario,id_libro, id_direccion, id_login, nombre, apellidos,numero_telefonico ,comentario, bandera):
            super().__init__(id_usuario,id_direccion, id_login, nombre, apellidos,numero_telefonico)  # Llamamos al constructor de la clase base
            self.id_comentario = id_comentario
            self.id_libro = id_libro
            self.comentario = comentario
            self.bandera = bandera



