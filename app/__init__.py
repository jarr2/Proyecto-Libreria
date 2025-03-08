from flask import Flask, jsonify, render_template, request, redirect,session, flash
from config import config
from flaskext.mysql import MySQL


from models.entities.Login import Login
from models.entities.Libro import Libro
from models.entities.Direccion import Direccion
from models.entities.Usuario import Usuario

from models.ModeloLogin import ModeloLogin
from models.ModeloLibro import ModeloLibro
from models.ModeloUsuario import ModeloUsuario
from models.ModeloDireccion import ModeloDireccion

from models.ConsultaApi import app_api

app = Flask(__name__)
app.config.from_object(config['development'])
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    if not session:
        print('Sin sesión')
        return render_template('login.html')
    else:
        print('con sesión ', session.values(), session.keys())
        if session['privilegio'] == None:
            session.pop('id_login', None)
            session.pop('privilegio', None)
            session.pop('id_direccion', None)
            session.pop('id_usuario', None)
            session.pop('message', None)
            session.pop('nombre', None)
            return redirect('/login')
        else:
            if session['privilegio'] == 'user':
                return render_template('home_usuario.html', nombre=session['nombre'])
            else:
                return render_template('home_admin.html', nombre=session['nombre'])



@app.route('/home', methods=['POST','GET'])
def entra():
    if request.method == 'POST':
        app_api
        login = Login(id_login=None,
                      correo=Login.encriptar(request.form.get('correo')),
                      contrasena=Login.encriptarContr(request.form.get('contrasena')),
                      privilegio=None)
        login = ModeloLogin.ConsultarLogin(mysql, login.correo, login.contrasena)
        print(login.privilegio)
        session['id_login'] = login.id_login
        session['privilegio'] = login.privilegio
        session['nombre'] = ModeloUsuario.Consultar_Nombre(mysql, session['id_login'])
        if login.privilegio == None:
            print(login.privilegio,'es igual a None')
            return redirect('/login')
        else:
            print(login.privilegio,'es diferente a None')
            if session['privilegio'] == 'user':
                return render_template('home_usuario.html', nombre=session['nombre'])
            elif session['privilegio'] == 'admin':
                return render_template('home_admin.html', nombre=session['nombre'])
    if request.method == 'GET':
        if not session:
            return redirect('/login')
        else:
            print(session.values())
            if session['privilegio'] == 'user':
                return render_template('home_usuario.html')
            else:
                return render_template('home_admin.html')
        
@app.route('/logout')
def logout():
    session.pop('id_login', None)
    session.pop('privilegio', None)
    session.pop('id_direccion', None)
    session.pop('id_usuario', None)
    session.pop('message', None)
    session.pop('nombre', None)
    print(session.values(), session.keys())
    return render_template('index.html', cerrarSesión=True)

@app.route('/mi-perfil', methods=['GET'])
def Mi_perfil():
    if not session:
            return redirect('/login')
    else:
        print(session.values())
        print("Variables existentes")
        if request.method == 'GET':
            usuario = ModeloUsuario.Consulta_Usuario(mysql, session['id_login'])
            session['id_direccion'] = usuario.id_direccion
            session['id_usuario'] = usuario.id_usuario
            print(session['nombre'])
            if usuario.id_usuario != None:
                direccion = ModeloDireccion.Consulta_Direccion(mysql, session['id_direccion'])
                return render_template('mi_perfil.html', usuario=usuario, direccion=direccion, nombre=session['nombre'])
            else:
                flash('No se pudieron cargar tus datos...')
                return render_template('mi_perfil.html', usuario=usuario, direccion=direccion, nombre=session['nombre'])

@app.route('/mi-perfil/editar', methods= ['GET'])
def editar_mi_perfil():
    if request.method == 'GET':
        if not session:
            return redirect('/login')
        else:
            print(session['id_login'])
            usuario = ModeloUsuario.Consulta_Usuario(mysql, session['id_login'])
            direccion = ModeloDireccion.Consulta_Direccion(mysql, session['id_direccion'])
            return render_template('editar_perfil.html', usuario=usuario, direccion=direccion, nombre=session['nombre'])
        
@app.route('/mi-perfil/actualizar', methods=['POST'])
def actualizar_mi_perfil():
    if request.method == 'POST':
        if not session:
            return redirect('/login')
        else:
           usuario = Usuario(id_usuario=session['id_usuario'],
                            id_direccion=session['id_direccion'],
                            id_login=session['id_login'],
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
                flash('Tus datos han sido actualizados')
                return redirect('/mi-perfil')
           else:
                flash('Algo ocurrió y tus datos no se actualizaron')
                return redirect('/mi-perfil')
        
@app.route('/usuarios', methods=['GET'])
def usuarios():
    if request.method == 'GET':
        usuarios = ModeloUsuario.Consultar_Usuarios(mysql)
        return render_template('usuarios.html', data=usuarios, nombre=session['nombre'])

@app.route('/usuarios/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
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
            flash('El usuario se actualizó con éxito')
            return redirect('/usuarios')
        else:
            flash('El usuario no se pudo actualizar')
            return redirect('/usuarios')
    return render_template('editar_usuario.html', login=login, usuario=usuario, nombre=session['id'])    

@app.route('/usuarios/crear', methods=['POST', 'GET'])
def crear_usuario():
    if request.method == 'POST':
        usuario = Usuario(nombre=request.form.get('nombres'), apellidos=request.form.get('apellidos'), numero_telefonico=request.form.get('telefono'),id_usuario=None, id_direccion=None, id_login=None)
        login = Login(correo=request.form.get('correo'),contrasena=Login.encriptarContr(request.form.get('contrasena')),privilegio='user', id_login=None)
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
            flash('Lo sentimos, el usuario no se creó con éxito.')
            return redirect('/usuarios')
    return render_template('crear_usuario.html', nombre=session['nombre'])

@app.route('/usuarios/eliminar/<int:id1>/<int:id2>/<int:id3>')
def eliminar_usuario(id1,id2,id3):
    #Id1 login, Id2 usuario, Id3 direccion
    ids = [id1,id2,id3]
    bandera = ModeloUsuario.Eliminar_un_Usuario(mysql,ids)
    if bandera == True:
         flash('El usuario se eliminó con éxito.','success')
         return redirect('/usuarios')
    else:
        flash('Lo sentimos, el usuario no se eliminó con éxito.','warning')
        return redirect('/usuarios')

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
    #print(datos)
    libro = Libro(id_libro=id, nombre=datos.nombre,editorial=datos.editorial,autor=datos.autor, stock=datos.stock, estatus=datos.estatus, precio=datos.precio, img_ruta=datos.img_ruta)
    #print(libro)
    return render_template("unLibro.html", libro=libro, nombre=session['nombre'])


if __name__ == '__main__':
    app.run()
