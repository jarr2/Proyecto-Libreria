from http.client import responses
import os
import urllib.parse
from flask import Flask, jsonify, render_template, request, redirect,session, flash, url_for
from config import config
from flaskext.mysql import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail
from werkzeug.utils import secure_filename
from emails import *
import requests

from models.entities.Login import Login
from models.entities.Libro import Libro
from models.entities.Direccion import Direccion
from models.entities.Ranking import Ranking
from models.entities.Usuario import Usuario
from models.entities.Libro_Comentado import Libro_Comentado

from models.ModeloLogin import ModeloLogin
from models.ModeloLibro import ModeloLibro
from models.ModeloUsuario import ModeloUsuario
from models.ModeloDireccion import ModeloDireccion
from models.ModeloLibroComentado import ModeloLibroComentado

from models.ConsultaApi import app_api

app = Flask(__name__)
UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config.from_object(config['development'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

carrito=[]
mysql = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail(app)


@login_manager_app.user_loader
def load_user(id):
    return ModeloLogin.Consultar_un_Login(mysql,id)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    print(session.keys(),session.values(), sep='\n')
    return render_template('login.html')


@app.route('/home', methods=['POST', 'GET'])
def entra():
    if request.method == 'POST':
        app_api
        login = Login(id=None,
                      correo=Login.encriptar(request.form.get('correo')),
                      contrasena=Login.encriptarContr(request.form.get('contrasena')),
                      privilegio=None)
        login = ModeloLogin.ConsultarLogin(mysql, login.correo, login.contrasena)
        if login.id != None:
            usuario_logueado = ModeloLogin.Consultar_un_Login(mysql,login.id)
            login_user(usuario_logueado)
            if login.privilegio == 'user':
                return render_template('home_usuario.html')
            elif login.privilegio == 'admin':
                return render_template('home_admin.html')
        else:
            flash('¡Correo o Contraseña incorrectos!', 'error')
            return redirect('/login')
    if request.method == 'GET':
        if current_user.login.privilegio == 'user':
            return render_template('home_usuario.html')
        elif current_user.login.privilegio == 'admin':
            return render_template('home_admin.html')
    else:
        return redirect('/login')
            
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('¡Tu sesión ha sido cerrada con éxito!', 'success')
    return redirect('/login')


@app.route('/mi-perfil', methods=['GET'])
@login_required
def Mi_perfil():
    if request.method == 'GET':
        usuario = ModeloUsuario.Consulta_Usuario(mysql, current_user.login.id)
        direccion = Direccion(calle=None, id_direccion=None, colonia=None, cp=None, estado=None, municipio=None, num_exterior=None, num_interior=None)
        if usuario.id_usuario != None:
            direccion = ModeloDireccion.Consulta_Direccion(mysql, usuario.id_direccion)
            return render_template('mi_perfil.html', usuario=usuario, direccion=direccion)
        else:
            flash('No se pudieron cargar tus datos...')
            return render_template('mi_perfil.html', usuario=usuario, direccion=direccion)
    else:
            return redirect('/home')

@app.route('/mi-perfil/editar', methods= ['GET'])
@login_required
def editar_mi_perfil():
    if request.method == 'GET':
        usuario = ModeloUsuario.Consulta_Usuario(mysql, current_user.login.id)
        direccion = ModeloDireccion.Consulta_Direccion(mysql, current_user.usuario.id_direccion)
        return render_template('editar_perfil.html', usuario=usuario, direccion=direccion)
    else:
        return render_template('/errores/401.html')

@app.route('/mi-perfil/actualizar', methods=['POST'])
@login_required
def actualizar_mi_perfil():
    if request.method == 'POST':
        usuario = Usuario(id_usuario=current_user.usuario.id_usuario,
                            id_direccion=current_user.usuario.id_direccion,
                            id_login=current_user.login.id,
                            nombre=request.form.get('nombres'),
                            apellidos=request.form.get('apellidos'),
                            numero_telefonico=request.form.get('num_telefonico'))
        direccion = Direccion(id_direccion=usuario.id_direccion,
                                calle=request.form.get('calle'),
                                estado=request.form.get('estado'),
                                municipio=request.form.get('municipio'),
                                colonia=request.form.get('colonia'),
                                cp=request.form.get('cp'),
                                num_interior=request.form.get('num_interior'),
                                num_exterior=request.form.get('num_exterior'))
        estatus = ModeloDireccion.Actualizar_Direccion(mysql,usuario,direccion)
        if estatus != False:
            flash('Tus datos han sido actualizados', 'success')
            return redirect('/mi-perfil')
        else:
            flash('Algo ocurrió y tus datos no se actualizaron', 'warning')
            return redirect('/mi-perfil')
        
@app.route('/usuarios', methods=['GET'])
@login_required
def usuarios():
    if request.method == 'GET':
        if current_user.login.privilegio == 'admin':
            usuarios = ModeloUsuario.Consultar_Usuarios(mysql)
            return render_template('usuarios.html', data=usuarios)
        else:
            return render_template('/errores/401.html')

@app.route('/usuarios/editar/<int:id>', methods=['POST', 'GET'])
@login_required
def editar_usuario(id):
    if current_user.login.privilegio == 'admin':
        bandera1 = False
        bandera2 = False
        login = ModeloLogin.Consultar_un_Login(mysql,id)
        usuario = ModeloUsuario.Consulta_Usuario(mysql, id)
        if request.method == 'POST':
            login.correo = request.form.get('correo')
            login.contrasena = Login.encriptarContr(request.form.get('contrasena'))
            usuario.nombre = request.form.get('nombre')
            usuario.apellidos = request.form.get('apellidos')
            usuario.numero_telefonico = request.form.get('telefono')
            bandera1 = ModeloLogin.Actualizar_un_Login(mysql,login)
            bandera2 = ModeloUsuario.Actualizar_un_Usuario(mysql,usuario)
            if bandera1 and bandera2 == True:
                flash('El usuario se actualizó con éxito', 'success')
                return redirect('/usuarios')
            else:
                flash('El usuario no se pudo actualizar', 'warning')
                return redirect('/usuarios')
        return render_template('editar_usuario.html', login=login, usuario=usuario)
    else:    
            return render_template('/errores/401.html')

@app.route('/usuarios/crear', methods=['POST', 'GET'])
@login_required
def crear_usuario():
    if current_user.login.privilegio == 'admin':
        if request.method == 'POST':
            usuario = Usuario(nombre=request.form.get('nombres'), apellidos=request.form.get('apellidos'), numero_telefonico=request.form.get('telefono'),id_usuario=None, id_direccion=None, id_login=None)
            login = Login(correo=request.form.get('correo'),contrasena=Login.encriptarContr(request.form.get('contrasena')),privilegio='user', id=None)
            direccion = Direccion(calle=request.form.get('calle'),
                                    estado=request.form.get('estado'),
                                    municipio=request.form.get('municipio'),
                                    colonia=request.form.get('colonia'),
                                    cp=request.form.get('cp'),
                                    num_interior=request.form.get('num_interior'),
                                    num_exterior=request.form.get('num_exterior'), id_direccion=None)
            bandera = ModeloUsuario.Crear_un_Usuario(mysql,login,usuario,direccion)
            if bandera == True:
                flash('El usuario se creó con éxito.','success')
                return redirect('/usuarios')
            else:
                flash('Lo sentimos, el usuario no se creó con éxito.', 'warning')
                return redirect('/usuarios')
        return render_template('crear_usuario.html')
    else:    
        return render_template('/errores/401.html')

@app.route('/usuarios/eliminar/<int:id1>/<int:id2>/<int:id3>')
@login_required
def eliminar_usuario(id1,id2,id3):
    #Id1 login, Id2 usuario, Id3 direccion
    if current_user.login.privilegio == 'admin':
        ids = [id1,id2,id3]
        bandera = ModeloUsuario.Eliminar_un_Usuario(mysql,ids)
        if bandera == True:
            flash('El usuario se eliminó con éxito.','success')
            return redirect('/usuarios')
        else:
            flash('Lo sentimos, el usuario no se eliminó con éxito.','warning')
            return redirect('/usuarios')
    else:
        return render_template('/errores/401.html')

@app.route('/libros', methods=['POST','GET'])
def MuestraLibros():
    if request.method == 'GET':
        libros = Libro(id_libro=None, nombre=None,editorial=None,autor=None, stock=None, estatus=None, precio=None, img_ruta=None)
        libros = ModeloLibro.ConsultarLibros(mysql)
        #print(libros)
        return libros

@app.route('/libros/<nombre_libro>')
def muestraUn_Libro(nombre_libro):
    id = request.args.get('id')
    datos = ModeloLibro.unLibro(mysql, id)
    datos_comentarios = ModeloLibroComentado.ConsultarLibroComentado(mysql, id)
    print(datos_comentarios)
    if datos_comentarios == []:
        calificar = 'Sincal'
    else:
        for dato in datos_comentarios:
            if(current_user.usuario.id_usuario == dato[1]):
                calificar = 'Calificado'
                break
            else:
                calificar = 'Sincal'
    #print(datos)
    libro = Libro(id_libro=id, nombre=datos.nombre,editorial=datos.editorial,autor=datos.autor, stock=datos.stock, estatus=datos.estatus, precio=datos.precio, img_ruta=datos.img_ruta)
    print(calificar)
    return render_template("unLibro.html", libro=libro, comentarios = datos_comentarios, calificar = calificar)

@app.route('/listaLibros')
def imprimeLibros():
    data = ModeloLibro.LibrosApi()
    return render_template("lista_libros.html",data=data)

@app.route('/actualizarLibro', methods=['POST', 'GET'])
@login_required
def actualizaLibro():
    if current_user.login.privilegio == 'admin':
        if request.method == 'GET':
            id = request.args.get('id')
            datos = ModeloLibro.unLibro(mysql, id)
            # print(datos)
            libro = Libro(id_libro=id, nombre=datos.nombre, editorial=datos.editorial, autor=datos.autor, stock=int(datos.stock),
            estatus=datos.estatus, precio=float(datos.precio), img_ruta=datos.img_ruta)
            return render_template("actualizarLibro.html",data=libro)
        elif request.method == 'POST':
            id = request.form.get('id')
            nombre = request.form.get('nombre')
            editorial = request.form.get('editorial')
            autor = request.form.get('autor')
            stock = request.form.get('stock')
            estatus = request.form.get('estatus')
            precio = request.form.get('precio')
            img_ruta = request.form.get('img_ruta')
            print(id)
            libro = Libro(id_libro=id, nombre=nombre, editorial=editorial, autor=autor,
                        stock=int(stock),
                        estatus=estatus, precio=float(precio),img_ruta=img_ruta)
            ModeloLibro.Actualizar_Libro(mysql, libro)
            data = ModeloLibro.LibrosApi()
            return render_template("lista_libros.html", data=data)
    else:
        return render_template('/errores/401.html')

@app.route('/eliminarLibro', methods=['POST', 'GET'])
@login_required
def eliminarLibro():
    if current_user.login.privilegio == 'admin':
        if request.method == 'GET':
            id = request.args.get('id')
            print(id)
            ModeloLibro.eliminarLibro(mysql, str(id))
            data = ModeloLibro.LibrosApi()
            return render_template("lista_libros.html", data=data)
    else:
        return render_template('/errores/401.html')

@app.route('/insertarLibro', methods=['POST'])
@login_required
def insertarLibro():
    if current_user.login.privilegio == 'admin':
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            editorial = request.form.get('editorial')
            autor = request.form.get('autor')
            stock = request.form.get('stock')
            estatus = request.form.get('estatus')
            precio = request.form.get('precio')
            print(request.files)
            if 'archivo' not in request.files:
                return 'No file part'
            file = request.files['archivo']
            if file.filename == '':
                return 'No selected file'
            if file:
                filename = file.filename
                save_path = os.path.join("static/img/", filename)
                img_ruta = save_path
                file.save(save_path)
            print(img_ruta)
            libro = Libro(id_libro="A1001", nombre=nombre, editorial=editorial, autor=autor,
                        stock=int(stock),
                        estatus=estatus, precio=float(precio), img_ruta=img_ruta)
            ModeloLibro.insertarLibro(mysql, libro)

            return imprimeLibros()
    else:
        return render_template('/errores/401.html')

@app.route('/Guardar_calificacion', methods=['GET','POST'])
#@login_required
def Guardar_calificacion():
    if request.method == 'POST':
        id_libro = request.args.get('id')
        ranking = request.form.get('ranking')
        id_usuario = current_user.usuario.id_usuario
        #cantidad_calificaciones = 1
        ranking = int(ranking)
        rankings = Ranking(id_ranking=None,id_usuario=id_usuario,id_libro=id_libro, ranking=ranking, cantidad_calificaciones=None)
        modelo_libro = ModeloLibro()
        resultado = modelo_libro.Guardar_calificacion(mysql, rankings)

        if resultado:
            promedio = modelo_libro.calcular_promedio(mysql, id_libro)

            respuesta = {
                'status': 'success',
                'message': 'Calificación guardada correctamente',
                'promedio': promedio
            }
            return jsonify(respuesta), 200
        else:
            respuesta = {
                'status': 'error',
                'message': 'Hubo un problema al guardar la calificación'
            }
            return jsonify(respuesta), 500  # Error del servidor





@app.route('/comentaLibro', methods=['POST'])
@login_required
def comentarLibro():
        if request.method == 'POST':
            id_libro = request.form.get('id_libro')
            name_libro = request.form.get('nombre')
            id_usuario = current_user.usuario.id_usuario
            comentario = request.form.get('comentario')
            objeto = Libro_Comentado
            objeto.id_libro=id_libro
            objeto.id_usuario=id_usuario
            objeto.comentario=comentario
            objeto.bandera=True
            ModeloLibroComentado.comentar(mysql, objeto)
            dato1 = urllib.parse.quote(name_libro)
            return redirect(url_for('muestraUn_Libro', nombre_libro=dato1, id=id_libro))


@app.route('/get_carrito')
def get_carrito():
    carrito2 = session.get('carrito', {})
    return jsonify(carrito2)

@app.route('/remove_carrito', methods=['GET'])
def remove_carrito():
    print("Queso badota")
    id_cont = request.args.get('id_cont')
    carrito3 = session.get('carrito', [])
    print(session)
    print(carrito3)
    del (carrito3[int(id_cont)])
    del (carrito[int(id_cont)])
    print(carrito3)
    session['carrito'] = carrito3
    print(session)
    return jsonify(carrito3)

@app.route('/agregarCarrito', methods=['GET'])
@login_required
def agregarCarrito():
    id_libro = request.args.get('id')
    cantidad= request.args.get('cantidad')
    print(id_libro, cantidad)
    consulta = ModeloLibro.unLibroDic(mysql,id_libro)
    datos_indice = [cantidad,list(consulta)]
    print(consulta[0])
    lista = list(consulta)
    print(lista)
    pos = 0
    agregar = True
    for item in carrito:
        if lista in item:
            lista_nueva = item
            lista_nueva[0] = int(lista_nueva[0])+int(datos_indice[0])
            lista_nueva[0] = str(lista_nueva[0])
            carrito[pos] = lista_nueva
            agregar = False
            break
        pos = pos + 1
    if agregar != False:
        carrito.append(datos_indice)

    print(carrito)
    nombre = urllib.parse.quote(consulta[1])
    session['carrito'] = carrito
    return redirect(url_for('muestraUn_Libro',nombre_libro=nombre, id=id_libro))

@app.route('/enviar_correo', methods = ['GET'])
def Enviar_Correo():
    datos = session.get('carrito', {})
    dic = validacion_Stock(datos)
    no_stock = []
    if(dic['bool'] == []):
        messi = ModeloLibro()
        for item in carrito:
            messi.descontarStock(int(item[0]), item[1][0])
            print("Dile ya a tus papas que ya no vas a regresar")
            Mandar_Correo(mail, current_user, session)
            session['carrito'] = {}
        flash('Tu ticket ha sido enviado a tu correo','success')
    else:
        no_stock= dic["ids"]
        flash('Algunos productos no cuentan con stock', 'warning')
        print(no_stock, "yo confiaba en ti")
    return render_template('home_usuario.html',no_stock=no_stock)

def validacion_Stock(carrito):
    validacion = {
        "bool": [],
        "ids": []
    }
    libros = ModeloLibro()
    for item in carrito:
        resultado = libros.verificarExistencias(mysql,item[1][0],int(item[0]))
        if resultado != True:
            validacion["ids"].append(item[1][0])
            validacion["bool"].append(resultado)
    return validacion

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404

def pagina_no_autorizada(error):
    return render_template('errores/401.html'), 401

def metodo_no_permitido(error):
    return render_template('errores/405.html'), 405

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.register_error_handler(401, pagina_no_autorizada)
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, metodo_no_permitido)

    app.run()
