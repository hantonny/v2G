from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from validate_docbr import CPF
import re
from . import db

cpfval = CPF()

auth = Blueprint('auth', __name__)

@auth.route('/')
def login():
     return render_template('Login/index.html', user_current=current_user)

@auth.route('/login', methods=['POST'])
def login_post():
    cpf = request.form.get('cpf')
    password = request.form.get('password')

    user = User.query.filter_by(cpf=cpf).first()

    if not user or not check_password_hash(user.password, password):
        flash('Verifique seus dados de login e tente novamente.')
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.dashboard'))

@auth.route('/adduser')

def adduser():
    return render_template('AddUser/index.html', user_current=current_user)

@auth.route('/adduser', methods=['POST'])

def adduser_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    cpf = request.form.get('cpf')
    phone = request.form.get('phone')
    group = request.form.get('group')

    user = User.query.filter_by(cpf=cpf).first()
    if user:
        flash('CPF já cadastrado!', 'error')
        return redirect(url_for('auth.adduser'))

    validocpf = cpfval.validate(cpf)

    if validocpf == False:
        flash('CPF Inválido!', 'error')
        return redirect(url_for('auth.adduser'))

    validadornome = "^[a-zA-Z-\s]*$"

    statename = bool(re.match(validadornome, name))

    if statename == False:
        flash('Nome Inválido!', 'error')
        return redirect(url_for('auth.adduser'))

    validadorphone = "^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"

    statephone = bool(re.match(validadorphone, phone))

    if statephone == False:
         flash('Telefone Inválido!', 'error')
         return redirect(url_for('auth.adduser'))

    new_user = User(cpf=cpf, email=email, name=name, phone=phone, group=group, password=generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()

    flash('Usuário cadastrado com sucesso!', 'success')
    return redirect(url_for('auth.adduser'))

@auth.route('/listusers')
@login_required
def listusers():
    userall = User.query.all()
    return render_template('Listusers/index.html', user_current=current_user, userall=userall)

@auth.route('/deleteuser/<int:id>')
@login_required
def deleteuser(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('auth.listusers'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))