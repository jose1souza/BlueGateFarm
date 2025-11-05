from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db 
from app.models.user_model import Usuario 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@auth_bp.route('/login', methods=['POST'])
def fazer_login():
   
    return redirect(url_for('main.dashboard'))

@auth_bp.route('/cadastro', methods=['POST'])
def fazer_cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    password = request.form.get('password')

    usuario_existente = db.session.execute(
        db.select(Usuario).filter_by(email=email)
    ).scalar_one_or_none()
    
    if usuario_existente:
        flash('Este e-mail já está cadastrado. Tente fazer login.', 'danger')
        return redirect(url_for('auth.cadastro'))

    novo_usuario = Usuario(nome=nome, email=email)
    
    novo_usuario.set_password(password)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.index'))
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao cadastrar usuário: {e}")
        flash('Ocorreu um erro inesperado ao cadastrar. Tente novamente.', 'danger')
        return redirect(url_for('auth.cadastro'))