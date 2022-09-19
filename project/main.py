from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, json
from .models import User
from .models import Posto
from validate_docbr import CPF
import re
from . import db

cpfval = CPF()

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    lat = -20.4804790424554
    lng = -54.60424944457882
    return render_template('Dashboard/index.html', lat = lat, lng = lng, user_current=current_user)

@main.route('/addposto')
@login_required
def addposto():
     return render_template('Addposto/index.html', user_current=current_user)

@main.route('/addposto', methods=['POST'])
@login_required
def addposto_post():
    name = request.form.get('name')
    cidade = request.form.get('city')
    latitude = request.form.get('lat')
    longitude = request.form.get('log')

    posto = Posto.query.filter_by(lat=latitude, log=longitude).first()
    if posto:
        flash('Posto já cadastrado!', 'error')
        return redirect(url_for('main.addposto'))

    new_posto = Posto(name=name,cidade=cidade,lat=latitude,log=longitude)

    db.session.add(new_posto)
    db.session.commit()
    flash('Posto cadastrado com sucesso!', 'success')
    return redirect(url_for('main.addposto'))

@main.route('/listpostos')
@login_required
def listpostos():
    postoall = Posto.query.all()
    return render_template('Listpostos/index.html', user_current=current_user, postoall=postoall)

@main.route('/deleteposto/<int:id>')
@login_required
def deleteposto(id):
    Posto.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Posto excluído com sucesso!', 'success')
    return redirect(url_for('main.listpostos'))

@main.route('/minhaconta')
@login_required
def minhaconta():
    return render_template('MinhaConta/index.html', user_current=current_user)

@main.route('/minhaconta', methods=['POST'])
@login_required
def minhaconta_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    cpf = request.form.get('cpf')
    phone = request.form.get('phone')
    
    user = User.query.filter_by(cpf=current_user.cpf).first()

    validocpf = cpfval.validate(cpf)

    if validocpf == False:
        flash('CPF Inválido!', 'error')
        return redirect(url_for('main.minhaconta'))

    validadornome = "^[a-zA-Z-\s]*$"

    statename = bool(re.match(validadornome, name))

    if statename == False:
        flash('Nome Inválido!', 'error')
        return redirect(url_for('main.minhaconta'))

    validadorphone = "^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"

    statephone = bool(re.match(validadorphone, phone))

    if statephone == False:
        flash('Telefone Inválido!', 'error')
        return redirect(url_for('main.minhaconta'))
        
    user.name = name
    user.password = generate_password_hash(password, method='sha256')
    user.phone = phone
    user.email = email
    user.cpf = cpf
    
    db.session.commit()
        
    flash('Dados atualizados com sucesso!', 'success')
    return redirect(url_for('main.minhaconta'))