from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import select
from app import db
from app.models.cultura_model import Cultura
from app.models.cultivo_model import Cultivo
from datetime import datetime

cultivo_bp = Blueprint('cultivo', __name__)

@cultivo_bp.route('/cultivos', methods=['GET'])
@login_required
def listar_cultivos():
    """Lista todos os registros de cultivo."""
    try:
        cultivos = db.session.scalars(select(Cultivo).order_by(Cultivo.data_plantio.desc())).all()
        
        return render_template('cultivo/listar.html', 
                               cultivos=cultivos)
    except Exception as e:
        flash(f'Erro ao carregar dados de cultivo: {e}', 'danger')
        return render_template('cultivo/listar.html', cultivos=[])

@cultivo_bp.route('/cultivos/novo', methods=['GET', 'POST'])
@cultivo_bp.route('/cultivos/editar/<int:id_cultivo>', methods=['GET', 'POST'])
@login_required
def criar_ou_editar_cultivo(id_cultivo=None):
    """
    Trata a criação de um novo cultivo ou a edição de um existente.
    """
    cultivo = None
    
    if id_cultivo:
        cultivo = db.session.get(Cultivo, id_cultivo)
        if not cultivo:
            flash('Registro de Cultivo não encontrado.', 'danger')
            return redirect(url_for('cultivo.listar_cultivos'))

    culturas = db.session.scalars(select(Cultura).order_by(Cultura.nome)).all()

    if request.method == 'POST':
        id_cultura_fk = request.form.get('id_cultura_fk')
        data_plantio_str = request.form.get('data_plantio')
        data_colheita_str = request.form.get('data_colheita')
        producao_str = request.form.get('producao')
        data_plantio = datetime.strptime(data_plantio_str, '%Y-%m-%d').date() if data_plantio_str else None
        data_colheita = datetime.strptime(data_colheita_str, '%Y-%m-%d').date() if data_colheita_str else None
        producao = float(producao_str) if producao_str else None
        
        if not id_cultura_fk:
            flash('A Cultura deve ser selecionada.', 'warning')
            return redirect(request.url)

        try:
            if id_cultivo:
                cultivo.id_cultura_fk = int(id_cultura_fk)
                cultivo.data_plantio = data_plantio
                cultivo.data_colheita = data_colheita
                cultivo.producao = producao
                
                db.session.commit()
                flash(f'Cultivo de {cultivo.cultura.nome} (ID: {cultivo.id_cultivo}) atualizado com sucesso!', 'success')
            else:
                novo_cultivo = Cultivo(
                    id_cultura_fk=int(id_cultura_fk), 
                    data_plantio=data_plantio, 
                    data_colheita=data_colheita, 
                    producao=producao,
                )
                db.session.add(novo_cultivo)
                db.session.commit()
                flash(f'Novo Cultivo cadastrado com sucesso!', 'success')

            return redirect(url_for('cultivo.listar_cultivos'))

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar cultivo: {e}', 'danger')
            
    return render_template('cultivo/formulario.html', 
                           cultivo=cultivo, 
                           culturas=culturas, 
                           titulo=('Editar Cultivo' if cultivo else 'Novo Registro de Cultivo'))


@cultivo_bp.route('/cultivos/excluir/<int:id_cultivo>', methods=['POST'])
@login_required
def excluir_cultivo(id_cultivo):
    """Exclui um registro de cultivo do banco de dados."""
    
    cultivo = db.session.get(Cultivo, id_cultivo)

    if not cultivo:
        flash('Registro de Cultivo não encontrado.', 'danger')
        return redirect(url_for('cultivo.listar_cultivos'))

    try:
        nome_cultura = cultivo.cultura.nome if cultivo.cultura else 'ID sem Cultura'
        db.session.delete(cultivo)
        db.session.commit()
        flash(f'Cultivo de {nome_cultura} (ID: {cultivo.id_cultivo}) excluído com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir cultivo: {e}', 'danger')

    return redirect(url_for('cultivo.listar_cultivos'))