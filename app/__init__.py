from flask import Flask, jsonify, render_template, request, redirect
from config import config
from flaskext.mysql import MySQL

from models.ModeloLogin import ModeloLogin
from models.entities.Login import Login
from models.ModeloLibro import ModeloLibro
from models.entities.Libro import Libro
from models.ConsultaApi import app_api

app = Flask(__name__)
app.config.from_object(config['development'])
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/entra', methods=['POST'])
def entra():
    if request.method == 'POST':
        app_api
        login = Login(id_login=None,
                      correo=Login.encriptar(request.form.get('correo')),
                      contrasena=Login.encriptarContr(
                          request.form.get('contrasena')),
                      privilegio=None)
        login = ModeloLogin.ConsultarLogin(mysql, login.correo, login.contrasena)
        print(login)
        if login.id_login != None:
            if login.privilegio == 'user':
                return render_template('prueba.html')
            else:
                return render_template('prueba1.html')
        else:
            return redirect('/login')

@app.route('/libros', methods=['POST','GET'])
def MuestraLibros():
    if request.method == 'GET':
        libros = Libro(id_libro=None, nombre=None,editorial=None,autor=None, stock=None, estatus=None, precio=None, img_ruta=None)
        libros = ModeloLibro.ConsultarLibros(mysql)
        print(libros)
        return libros

@app.route('/libros/<nombre_libro>')
def muestraUn_Libro(nombre_libro):
    id = request.args.get('id')
    datos = ModeloLibro.unLibro(mysql, id)
    print(datos)
    libro = Libro(id_libro=id, nombre=datos.nombre,editorial=datos.editorial,autor=datos.autor, stock=datos.stock, estatus=datos.estatus, precio=datos.precio, img_ruta=datos.img_ruta)
    print(libro)
    return render_template("unLibro.html", libro=libro)


if __name__ == '__main__':
    app.run()
