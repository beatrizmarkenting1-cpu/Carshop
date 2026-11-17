from datetime import date
from models.models import Carro, db

STATUS_VALIDOS = ("disponivel", "vendido")


def _validar(marca, modelo, ano, quilometragem, preco, status):
    """Valida e converte os campos vindos do formulário."""
    marca = (marca or "").strip()
    modelo = (modelo or "").strip()

    if not marca or not modelo:
        raise ValueError("Marca e modelo são obrigatórios.")

    try:
        ano = int(ano)
    except (TypeError, ValueError):
        raise ValueError("Ano inválido.")
    if ano < 1886 or ano > date.today().year + 1:
        raise ValueError("Ano fora do intervalo permitido.")

    try:
        quilometragem = int(quilometragem or 0)
    except (TypeError, ValueError):
        raise ValueError("Quilometragem inválida.")
    if quilometragem < 0:
        raise ValueError("A quilometragem não pode ser negativa.")

    try:
        preco = float(str(preco).replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Preço inválido.")
    if preco <= 0:
        raise ValueError("O preço deve ser maior que zero.")

    if status not in STATUS_VALIDOS:
        status = "disponivel"

    return marca, modelo, ano, quilometragem, preco, status


def create_car(usuario_id, marca, modelo, ano, cor, quilometragem, preco, descricao, status="disponivel") -> Carro:
    marca, modelo, ano, quilometragem, preco, status = _validar(
        marca, modelo, ano, quilometragem, preco, status
    )

    carro = Carro(
        marca=marca,
        modelo=modelo,
        ano=ano,
        cor=(cor or "").strip() or None,
        quilometragem=quilometragem,
        preco=preco,
        descricao=(descricao or "").strip() or None,
        status=status,
        usuario_id=usuario_id,
    )
    db.session.add(carro)
    db.session.commit()
    return carro


def get_cars_by_user(usuario_id: int) -> list[Carro]:
    return (
        db.session.query(Carro)
        .filter_by(usuario_id=usuario_id)
        .order_by(Carro.id.desc())
        .all()
    )


def get_car_by_id(car_id: int, usuario_id: int) -> Carro:
    """Busca o carro apenas se pertencer ao usuário informado."""
    return db.session.query(Carro).filter_by(id=car_id, usuario_id=usuario_id).first()


def update_car(car_id, usuario_id, marca, modelo, ano, cor, quilometragem, preco, descricao, status) -> Carro:
    carro = get_car_by_id(car_id, usuario_id)
    if not carro:
        raise ValueError("Carro não encontrado.")

    marca, modelo, ano, quilometragem, preco, status = _validar(
        marca, modelo, ano, quilometragem, preco, status
    )

    carro.marca = marca
    carro.modelo = modelo
    carro.ano = ano
    carro.cor = (cor or "").strip() or None
    carro.quilometragem = quilometragem
    carro.preco = preco
    carro.descricao = (descricao or "").strip() or None
    carro.status = status
    db.session.commit()
    return carro


def delete_car(car_id: int, usuario_id: int) -> None:
    carro = get_car_by_id(car_id, usuario_id)
    if not carro:
        raise ValueError("Carro não encontrado.")

    db.session.delete(carro)
    db.session.commit()
