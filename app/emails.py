from flask_mail import Message
from flask import current_app, render_template

def Mandar_Correo(mail, current_user, data):
    try:
        message = Message('Confirmación de compra de libro',
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[current_user.login.correo, '20223tn106@utez.edu.mx'])
        message.html = render_template('mails/confirmacion_compra.html',current_user=current_user, data=data)
        mail.send(message)
    except Exception as ex:
        raise Exception(ex)
