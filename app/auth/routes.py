from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db 
from app.models.user_model import Usuario 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    # Se o usuário já estiver logado, redireciona para o dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@auth_bp.route('/login', methods=['POST'])
def fazer_login():
    email = request.form.get('email')
    password = request.form.get('password')

    # 1. Busca o usuário pelo e-mail
    usuario = db.session.execute(
        db.select(Usuario).filter_by(email=email)
    ).scalar_one_or_none()
    
    # 2. Verifica se o usuário existe E se a senha confere
    if usuario and usuario.check_password(password):
        # Loga o usuário usando Flask-Login e o mantém logado (remember=True)
        login_user(usuario, remember=True)
        flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
        # Redireciona para o dashboard
        return redirect(url_for('main.dashboard'))
    else:
        # Mensagem de erro e volta para a tela de login
        flash('E-mail ou senha incorretos.', 'danger')
        return redirect(url_for('auth.index'))


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

@auth_bp.route('/logout')
def logout():
    # Finaliza a sessão do usuário
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.index'))