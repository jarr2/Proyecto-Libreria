from flask import Flask, jsonify, render_template, request, redirect
from config import config
from flaskext.mysql import MySQL

from models.ModeloLogin import ModeloLogin
from models.entities.Login import Login


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


if __name__ == '__main__':
    app.run()
