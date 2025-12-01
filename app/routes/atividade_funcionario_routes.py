from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import select
from app import db
from app.models.funcionario_model import Funcionario
from app.models.atividade_funcionario_model import AtividadeFuncionario
from datetime import datetime

atividade_funcionario_bp = Blueprint('atividade_funcionario', __name__)

@atividade_funcionario_bp.route('/atividades_funcionario', methods=['GET'])
@login_required
def listar_atividades():
    """Lista todos os registros de atividade de funcionários."""
    try:
        atividades = db.session.scalars(select(AtividadeFuncionario).order_by(AtividadeFuncionario.data.desc())).all()
        
        funcionarios = db.session.scalars(select(Funcionario).order_by(Funcionario.nome)).all()
        
        return render_template('atividade_funcionario/listar.html', 
                               atividades=atividades,
                               funcionarios=funcionarios)
    except Exception as e:
        flash(f'Erro ao carregar dados de atividades: {e}', 'danger')
        return render_template('atividade_funcionario/listar.html', atividades=[], funcionarios=[])


@atividade_funcionario_bp.route('/atividades-funcionario/novo', methods=['GET', 'POST'])
@atividade_funcionario_bp.route('/atividades-funcionario/editar/<int:id_atividade>', methods=['GET', 'POST'])
@login_required
def criar_ou_editar_atividade(id_atividade=None):
    """
    Trata a criação de um novo registro de atividade ou a edição de um existente.
    """
    atividade = None
    
    if id_atividade:
        atividade = db.session.get(AtividadeFuncionario, id_atividade)
        if not atividade:
            flash('Registro de Atividade não encontrado.', 'danger')
            return redirect(url_for('atividade_funcionario.listar_atividades'))

    funcionarios = db.session.scalars(select(Funcionario).order_by(Funcionario.nome)).all()

    if request.method == 'POST':
        id_funcionario = request.form.get('id_funcionario')
        data_str = request.form.get('data')
        descricao = request.form.get('descricao')
        horas_trabalhadas_str = request.form.get('horas_trabalhadas')
        
        data_atividade = datetime.strptime(data_str, '%Y-%m-%d').date() if data_str else None
        horas_trabalhadas = float(horas_trabalhadas_str) if horas_trabalhadas_str else None
        
        if not id_funcionario or not data_atividade:
            flash('O Funcionário e a Data são campos obrigatórios.', 'warning')
            return redirect(request.url)

        try:
            if id_atividade:
                atividade.id_funcionario = int(id_funcionario)
                atividade.data = data_atividade
                atividade.descricao = descricao
                atividade.horas_trabalhadas = horas_trabalhadas
                
                db.session.commit()
                flash(f'Atividade de {atividade.funcionario.nome} atualizada com sucesso!', 'success')
            else:
                nova_atividade = AtividadeFuncionario(
                    id_funcionario=int(id_funcionario), 
                    data=data_atividade, 
                    descricao=descricao, 
                    horas_trabalhadas=horas_trabalhadas,
                )
                db.session.add(nova_atividade)
                db.session.commit()
                flash(f'Nova Atividade cadastrada com sucesso!', 'success')

            return redirect(url_for('atividade_funcionario.listar_atividades'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar atividade: {e}', 'danger')
            
    return render_template('atividade_funcionario/formulario.html', 
                           atividade=atividade, 
                           funcionarios=funcionarios, 
                           titulo=('Editar Atividade' if atividade else 'Novo Registro de Atividade'))


@atividade_funcionario_bp.route('/atividades-funcionario/excluir/<int:id_atividade>', methods=['POST'])
@login_required
def excluir_atividade(id_atividade):
    """Exclui um registro de atividade do banco de dados."""
    
    atividade = db.session.get(AtividadeFuncionario, id_atividade)

    if not atividade:
        flash('Registro de Atividade não encontrado.', 'danger')
        return redirect(url_for('atividade_funcionario.listar_atividades'))

    try:
        nome_funcionario = atividade.funcionario.nome if atividade.funcionario else 'ID sem Funcionário'
        data_atividade = atividade.data.strftime('%d/%m/%Y')
        db.session.delete(atividade)
        db.session.commit()
        flash(f'Atividade de {nome_funcionario} em {data_atividade} excluída com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir atividade: {e}', 'danger')

    return redirect(url_for('atividade_funcionario.listar_atividades'))