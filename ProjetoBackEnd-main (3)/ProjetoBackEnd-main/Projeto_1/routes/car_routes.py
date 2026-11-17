from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from services.car_service import (
    create_car, get_cars_by_user, get_car_by_id, update_car, delete_car
)
from .auth_decorator import login_required

car_bp = Blueprint('car', __name__, url_prefix='/carros', template_folder='templates')

CAMPOS = ('marca', 'modelo', 'ano', 'cor', 'quilometragem', 'preco', 'descricao', 'status')


@car_bp.route('/')
@login_required
def listar_carros():
    carros = get_cars_by_user(session['user_id'])
    return render_template('carros.html', carros=carros)


@car_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_carro():
    if request.method == 'POST':
        dados = {campo: request.form.get(campo, '') for campo in CAMPOS}
        try:
            create_car(session['user_id'], **dados)
            flash("Carro cadastrado com sucesso!", "success")
            return redirect(url_for('car.listar_carros'))
        except ValueError as e:
            flash(str(e), "danger")
            # reexibe o formulário preservando o que foi digitado
            return render_template('carro_form.html', carro=dados, editando=False)

    return render_template('carro_form.html', carro={'status': 'disponivel'}, editando=False)


@car_bp.route('/editar/<int:car_id>', methods=['GET', 'POST'])
@login_required
def editar_carro(car_id):
    carro = get_car_by_id(car_id, session['user_id'])
    if not carro:
        flash("Carro não encontrado.", "danger")
        return redirect(url_for('car.listar_carros'))

    if request.method == 'POST':
        dados = {campo: request.form.get(campo, '') for campo in CAMPOS}
        try:
            update_car(car_id, session['user_id'], **dados)
            flash("Carro atualizado com sucesso!", "success")
            return redirect(url_for('car.listar_carros'))
        except ValueError as e:
            flash(str(e), "danger")
            dados['id'] = car_id
            return render_template('carro_form.html', carro=dados, editando=True)

    return render_template('carro_form.html', carro=carro, editando=True)


@car_bp.route('/excluir/<int:car_id>', methods=['POST'])
@login_required
def excluir_carro(car_id):
    try:
        delete_car(car_id, session['user_id'])
        flash("Carro removido.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('car.listar_carros'))
