from models.entities.Usuario import Usuario
from models.entities.Login import Login
from flask_login import UserMixin


class LoginUser(UserMixin):
    def __init__(self, Login, Usuario):
        self.login = Login
        self.usuario = Usuario
        self.id = Login.id