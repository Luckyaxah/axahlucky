from flask import Blueprint, render_template, request, current_app, redirect, url_for

from axahlucky.emails import send_hello_mail

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/hello')
def email_hello():
    send_hello_mail()
    return redirect(url_for('main.info'))
